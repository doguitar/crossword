<!DOCTYPE html>
<html lang="en">
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
		<link rel="stylesheet" href="${base}css/jquery-ui.min.css">
		<link rel="stylesheet" href="${base}css/bootstrap.min.css">
		<link rel="stylesheet" href="${base}css/bootstrap-theme.min.css">
		<link rel="stylesheet" href="${base}css/style.css">
        <%block name="css_block"></%block>
		<script type="text/javascript" >var _base = "${base}";</script>
		<script src="${base}js/jquery-1.10.2.min.js" ></script>
		<script src="${base}js/jquery-ui.min.js"></script>
		<script src="${base}js/bootstrap.min.js"></script>
		<script src="${base}js/ifvisible.min.js"></script>
		<script src="${base}js/script.js"></script>
        <%block name="js_block"></%block>
        <title><%block name="title_block">&#9773; CCCP &#9773;</%block></title>
	</head>
	<body style="">
    <%block name="nav_block">
    </%block>
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