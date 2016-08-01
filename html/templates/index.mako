<%inherit file="/base.mako"/>
<%namespace name="nav" file="/nav.mako"/>
<%block name="nav_block">
    ${nav.make_nav('')}
</%block>
<div style="text-align: center;">
	% if not username:
        <%block name="js_block">
        <script src="${base}js/crypto/rollups/sha3.js"></script>
        <script src="${base}js/login.js"></script>
        </%block>
        <%namespace name="login" file="/login.mako"/>
            ${login.login()}
    % else:
        <%namespace name="select" file="/select.mako"/>
            ${select.select(datetime.datetime.today())}
    % endif
</div>