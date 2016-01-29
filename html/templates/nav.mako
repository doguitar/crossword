<%def name="make_nav(selected)">
<%
	nav_links = [
		#['sql', base+'sql', ''],
		#['crypto', base+'crypto', '']
	]
%>
<nav class="navbar navbar-inverse navbar-static-top">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="${base}" title="Comrade's Concurrent Crossword Puzzles" style="margin-left: 0;">&#9773; CCCP &#9773;</a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
                % for name, link, role in nav_links:
                <li class="${"active" if name == selected else ""}"><a href="${link}" role="${role}">${name}</a></li>
                % endfor
            </ul>
        </div>
    </div>
</nav>
</%def>