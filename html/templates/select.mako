<%def name="select(startdate)">
<div class="calendar">
% for w in sorted(range(-4, 1), reverse=True):
    <% monday = startdate - datetime.timedelta(days=startdate.weekday()) + datetime.timedelta(days=w*7) %>
    <div class="week">
        % for d in range(0, 7):
            <% today = (monday + datetime.timedelta(days=d)).date() %>
            <div class="day">
                <div class="date">${today}</div>
                % for c in crosswords.get(today, []):
                    <a href="${base}crossword/${c.get("Id")}">${c.get("Title")}</a>
                % endfor
            </div>
        % endfor
    </div>
% endfor
    <div class="week"></div>
</div>


</%def>