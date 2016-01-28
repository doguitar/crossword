<%inherit file="/base.mako"/>
<%namespace name="nav" file="/nav.mako"/>
<%block name="nav_block">
    ${nav.make_nav('')}
</%block>
<div style="text-align: center;">
	% if not username:
	<form action="${base}login">
		<input type="text" name="username" placeholder="username" />
		<input type="hidden" name="r" value="${return_url}" />
	</form>
    % else:
	<select id="puzzle">
		<option></option>
		% for c in crosswords:
		<option value="${c["Id"]}">${c["Title"]}</option>
		% endfor
	</select>
    % endif
</div>