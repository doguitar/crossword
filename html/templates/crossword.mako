<%inherit file="/base.mako"/>
<% cell_size = 100/float(puzzle["height"])
%>
<%namespace name="nav" file="/nav.mako"/>
<%block name="nav_block">
    ${nav.make_nav('')}
</%block>
<%block name="title_block">
    ${puzzle["title"]}
</%block>
<script type="text/javascript">
	var clues = ${clues};
</script>
<style>
	@media all and (orientation:landscape) {
		.cell {
			width: ${cell_size}%;
			height: ${cell_size}%;
		}
	}
	@media all and (orientation:portrait) {
		.cell {
			width: ${cell_size}%;
			height: ${cell_size}%;
		}
	}
	.crossword{
		font-size: ${cell_size}vmin;
	}
</style>
<div style="text-align: center;" id="focus">
	<div id="crossword_container">
		<table style="width:100%;" class="crossword">
			<%
				rows = puzzle["rows"]
			%>
			% for y in range(0, len(rows)):
			<%
				r = rows[y]
			%>
				<tr>
			% for x in range(0, len(r)):
			<%
				c = r[x]
			%>
				<td x="${x}" y="${y}" class="cell x${x}y${y} ${"black" if c["black"] else ""}" >
					<div class="content">
						% if not c["black"]:
						% if c["clue"]:
						<div class="clue">${c["clue"]}</div>
						% endif
						<span class="text answer"></span>
						% endif
					</div>
				</td>
			% endfor
				</tr>
			% endfor
		</table>
	<div style=" width:100%;">
		<div class="clue primary"></div>
		<div class="clue secondary"></div>
	</div>
	</div><div id="clear" style="clear:both;"></div><!--
    --><table id="left_keyboard" class="keyboard">
		<tr><td>Q</td><td>W</td><td>E</td><td>R</td><td>T</td></tr>
		<tr><td>A</td><td>S</td><td>D</td><td>F</td><td>G</td></tr>
		<tr><td></td><td>Z</td><td>X</td><td>C</td><td>V</td></tr>
		<tr><td></td><td></td><td></td><td></td><td>del</td></tr>
	</table><!--
    --><table id="right_keyboard" class="keyboard">
		<tr><td>Y</td><td>U</td><td>I</td><td>O</td><td>P</td></tr>
		<tr><td>H</td><td>J</td><td>K</td><td>L</td><td></td></tr>
		<tr><td>B</td><td>N</td><td>M</td><td>&uarr;</td><td></td></tr>
		<tr><td>del</td><td></td><td>&larr;</td><td>&darr;</td><td>&rarr;</td></tr>
	</table><!--

--></div>