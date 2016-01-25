<%inherit file="/base.mako"/>


<div style="text-align: center;">
	% if not username:
	<form action="${base}login">
		<input type="text" name="username" />
	</form>

    % else:


	<select id="puzzle">
		<option></option>
		% for c in crosswords:
		<option value="${base}crossword/${c["Id"]}">${c["Title"]}</option>
		% endfor
	</select>
    % endif
</div>