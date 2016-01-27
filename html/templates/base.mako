<% 	
	nav_links = [
		#['sql', base+'sql', '', '']
	]
%>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        <title>&#9773; CCCP &#9773;</title>
		<link rel="stylesheet" href="${base}css/style.css">
		<link rel="stylesheet" href="${base}css/bootstrap.min.css">
		<link rel="stylesheet" href="${base}css/bootstrap-theme.min.css">
		<script type="text/javascript" >var _base = "${base}";</script>
		<script src="https://code.jquery.com/jquery-1.10.2.min.js" ></script>
		<script src="${base}js/bootstrap.min.js"></script>
		<script src="${base}js/script.js"></script>
	</head>
	<body style="">
<nav class="navbar navbar-inverse navbar-static-top">
	<div class="container-fluid">
		<div class="navbar-header">
			<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
			<a class="navbar-brand" href="${base}" title="Comrade's Communal Crossword Puzzles" style="margin-left: 0;">&#9773; CCCP &#9773;</a>
		</div>
		<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
			<ul class="nav navbar-nav">
				% for name, link, role, cls in nav_links:
				<li><a href="${link}" role="${role}" class="${cls}">${name}</a></li>	
				% endfor
			</ul>		
		</div><!-- /.navbar-collapse -->
	</div><!-- /.container-fluid -->
</nav>
<div class="container-fluid" role="main">
${self.body()}
</div>
</body>
</html>
<%def name="pager(ps, p, c, mask)">

<% 		
	display_count = 5 - 1
	max = int(c / ps) + 1
	
	pager_min = p - (display_count/2) if p - (display_count/2) > 0 else 1
	pager_max = pager_min + display_count if pager_min + display_count <= max else max
	
	width = 90/(display_count+5)
%>
% if max > 1:
<nav style="text-align: center;">
  <ul class="pagination pagination-lg">	
    <li class="${'disabled' if p==1 else ''}" style="width: ${width}px;">
      <a href="${mask.format(1)}" aria-label="Previous">
        <span aria-hidden="true" class="glyphicon glyphicon-fast-backward"></span>
      </a>
    </li>
    <li class="${'disabled' if p-1<1 else ''}" style="width: ${width}px;">
      <a href="${mask.format(p-1)}" aria-label="Previous">
        <span aria-hidden="true" class="glyphicon glyphicon-backward"></span>
      </a>
    </li>
	% for i in range(pager_min, pager_max+1):
    <li class="${'disabled' if p==i else ''}" style="width: ${width}px;"><a href="${mask.format(i)}">${i}</a></li>
	% endfor
    <li class="${'disabled' if p+1>max else ''}" style="width: ${width}px;">
      <a href="${mask.format(p+1)}" aria-label="Next">
        <span aria-hidden="true" class="glyphicon glyphicon-forward"></span>
      </a>
    </li>
    <li class="${'disabled' if p==max else ''}" style="width: ${width}px;">
      <a href="${mask.format(max)}" aria-label="Next">
        <span aria-hidden="true" class="glyphicon glyphicon-fast-forward"></span>
      </a>
    </li>
  </ul>
</nav>
% endif
</%def>