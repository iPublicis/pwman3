% rebase('base.tpl')
%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<form action="/" method="POST">
<select multiple name="tag" onchange="this.form.submit()">
%for tag in tags:
<option value="{{tag}}">{{tag}}</option>
%end
</select>
</form>
<p>Click on username to view the details:</p>
<table border="1">
%for node in nodes:
<tr>
  %#for item in node:
  %# <td><a href={{node._id}}><{{item}}</a></td>
  <td><a href=/node/{{node._id}}>{{node.username}}@{{node.url}}</a></td>
  <td>{{  ', '.join([t.strip() for t in filter(None, node.tags)]) }}</td>
  <td><a href="/edit/{{node._id}}>edit</td>
  %end
  </tr>
%end
</table>