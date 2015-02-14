# ============================================================================
# This file is part of Pwman3.
#
# Pwman3 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2
# as published by the Free Software Foundation;
#
# Pwman3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pwman3; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ============================================================================
# Copyright (C) 2012-2014 Oz Nahum Tiram <nahumoz@gmail.com>
# ============================================================================
# Copyright (C) 2006 Ivan Kelly <ivan@ivankelly.net>
# ============================================================================

"""
Factory to create Database instances
A Generic interface for all DB engines.
Usage:

import pwman.data.factory as DBFactory

db = DBFactory.create(params)
db.open()
.....
"""
import sys
if sys.version_info.major > 2:  # pragma: no cover
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from pwman.data.database import DatabaseException
from pwman.data.drivers import sqlite


def check_db_version(ftype, filename):
    if ftype == "SQLite":
        ver = sqlite.SQLite.check_db_version(filename)
        try:
            return float(ver.strip("\'"))
        except ValueError:
            return 0.3
    # TODO: implement version checks for other supported DBs.
    if ftype == "Postgresql":
        ver = sqlite.PostgresqlDatabase.check_db_version(filename)


def create(dbtype, version=None, filename=None):
    """
    create(params) -> Database
    Create a Database instance.
    'type' can only be 'SQLite' at the moment
    """
    if dbtype == "SQLite":
        from pwman.data.drivers import sqlite
        if str(version) == '0.6':
            db = sqlite.SQLite(filename)
        else:
            db = sqlite.SQLite(filename, dbformat=version)

    elif dbtype == "Postgresql":  # pragma: no cover
        try:
            from pwman.data.drivers import postgresql
            db = postgresql.PostgresqlDatabase()
        except ImportError:
            raise DatabaseException("python-psycopg2 not installed")
    elif dbtype == "MySQL":  # pragma: no cover
        try:
            from pwman.data.drivers import mysql
            db = mysql.MySQLDatabase()
        except ImportError:
            raise DatabaseException("python-mysqldb not installed")
    else:
        raise DatabaseException("Unknown database type specified")
    return db


def createdb(dburi, version):
    dburi = urlparse(dburi)
    dbtype = dburi.scheme
    filename = dburi.path

    if dbtype == "sqlite":
        from pwman.data.drivers import sqlite
        if str(version) == '0.6':
            db = sqlite.SQLite(filename)
        else:
            db = sqlite.SQLite(filename, dbformat=version)

    elif dbtype == "postgresql":
        try:
            from pwman.data.drivers import postgresql
            db = postgresql.PostgresqlDatabase(dburi)
        except ImportError:
            raise DatabaseException("python-psycopg2 not installed")
    elif dbtype == "mysql":  # pragma: no cover
        try:
            from pwman.data.drivers import mysql
            db = mysql.MySQLDatabase()
        except ImportError:
            raise DatabaseException("python-mysqldb not installed")
    else:
        raise DatabaseException("Unknown database type specified")
    return db
