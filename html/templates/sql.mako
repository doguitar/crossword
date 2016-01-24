<%inherit file="/base.mako"/>
<script type="text/javascript">
	function grow_input(){
		var input = $("#sql");
		if(input.get(0).scrollHeight > input.height()+5)
			input.height(input.get(0).scrollHeight+5);
	}

	$(document).ready(function(){
        grow_input();
		$("#sql").keyup(grow_input);
    });
</script>

<form action="${base}test" method="get">
	<textarea name="sql" id="sql" style="width:100%" rows="10">${sql if sql else ""}</textarea>
	<input type="submit" value="submit" />
</form>
<span>${elapsed}</span>

% if rows:
<table class="table table-bordered table-striped">
	% if len(rows) > 0:	
	<tr>
		% for h in rows[0].keys():
		<th>${h}</th>
		%endfor
	</tr>
	%endif
	% for i in range(0, len(rows)):
	<tr class="${'alt' if i % 2 == 1 else ''}">
		% for c in rows[i]:		
		<td>${c}</td>		
		%endfor
	</tr>
	%endfor
</table>
%endif