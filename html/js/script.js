$(function() {
    $("select#puzzle").change(function(){
        document.location = _base + "crossword/" + $(this).val();
    });
    if ($(".crossword").length > 0) {
        $(".crossword .cell").click(function () {
            var cell = $(this);
            if (cell.hasClass("primary") && cell.hasClass("secondary"))
                toggle_vert(this);
            else {
                select_cell(cell);
            }
        });
        $(".keyboard td").click(function () {
            if(navigator && navigator.vibrate) navigator.vibrate([100]);
            var key = $(this).text();
            var cell = $(".cell.primary.secondary");
            switch (key) {
                case "":
                    toggle_vert(cell);
                    break;
                case "↓":
                    move_cell(cell, 1, true);
                    break;
                case "←":
                    move_cell(cell, -1, false);
                    break;
                case "↑":
                    move_cell(cell, -1, true);
                    break;
                case "→":
                    move_cell(cell, 1, false);
                    break;
                case "del":
                    write_letter("");
                    move_cell(cell, -1, $(".crossword").hasClass("vert"));
                    break;
                default:
                    write_letter(key);
                    move_cell(cell, 1, $(".crossword").hasClass("vert"));
                    break;
            }
        });
        $(document.body).keydown(function (e) {
            if (e.ctrlKey || e.altKey) return;

            var code = e.keyCode || e.which;
            console.log(code);
            var cell = $(".cell.primary.secondary");
            switch (code) {
                case 32: //space
                    toggle_vert(cell);
                    break;
                case 8: //backspace
                case 46: //delete
                    write_letter("");
                    move_cell(cell, -1, $(".crossword").hasClass("vert"));
                    e.preventDefault();
                    break;
                case 39: //right
                    move_cell(cell, 1, false);
                    e.preventDefault();
                    break;
                case 37: //left
                    move_cell(cell, -1, false);
                    e.preventDefault();
                    break;
                case 38: //up
                    move_cell(cell, -1, true);
                    e.preventDefault();
                    break;
                case 40: //down
                    move_cell(cell, 1, true);
                    e.preventDefault();
                    break;
                default:
                    if (is_letter(code)) {
                        write_letter(String.fromCharCode(code));
                        move_cell(cell, 1, $(".crossword").hasClass("vert"));
                    }
            }
        });
        $(".cell").css("font-size", $(".cell").height() + "px");
        $(window).resize(function () {
            $(".cell").css("font-size", $(".cell").height() + "px");
        });
        highlight($(".cell").first());
        $(document.body).scrollTop($(".crossword").offset.top);

        function update_crossword() {
            if (!updating) {
                updating = true;
                $.get(
                    _base + "json/moves",
                    {
                        "session_id": window.location.pathname.split("/").pop(),
                        "since": since
                    }
                ).success(function (data) {
                    console.log(data);
                    for (var i = 0; i < data.length; i++) {
                        var move = data[i];

                        var cell = $(".x" + move.X + "y" + move.Y);

                        var currentColor = cell.css('backgroundColor');
                        var toColor = get_color(move.UserHash);

                        cell
                            .css({backgroundColor: toColor})
                            .animate({backgroundColor: currentColor}, 800,
                                function(){$(this).css('background-color', '');});
                        cell.find(".answer").text(move.Letter);

                        if (move.Id > since) since = move.Id;
                    }
                }).always(function(){ updating = false; });
            }
        }
        ifvisible.onEvery(0.5, function(){
            update_crossword();
        });
    }
});
function get_color(user_hash){
    var index = users.indexOf(user_hash);
    if (index < 0){
        users.push(user_hash);
        generate_colors();
    }
    return colors[index];
}
function generate_colors(){
    colors = [];
    var e = 0.618033988749895;
    for (var i = 0; i < users.length; i++){
        var c = HSVtoRGB(e*i % 1.0, 0.5, 1.0);
        colors.push("rgb("+[c.r,c.g,c.b].join()+")");
    }
}
function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (arguments.length === 1) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}
var colors = [];
var users = [];
var updating = false;
var since = 0;
function clear_highlights(){
    $(".cell.primary").removeClass("primary")
    $(".cell.secondary").removeClass("secondary");
}

function select_cell(cell) {
    if (!$(cell).hasClass("black")) {
        clear_highlights();
        highlight(cell);
    }
}

function write_letter(char){
    var cell = $(".cell.primary.secondary .answer");
    var x = cell.parents("td").attr("x");
    var y = cell.parents("td").attr("y");

    $.get(
        _base + "json/move",
        {
            "cord_x" : x,
            "cord_y" : y,
            "char" : char,
            "session_id" : window.location.pathname.split("/").pop()
        }
    );

    cell.text(char);
}

function toggle_vert(cell){
    $(cell).parents("table").toggleClass("vert");
    clear_highlights();
    highlight(cell);
}

function move_cell(cell, count, vert){
    cell =  $(cell);
    var x = parseInt(cell.attr("x"));
    var y = parseInt(cell.attr("y"));

    do{
        if(vert) y += count;
        else x += count;
        cell = $(".x"+x+"y"+y+"");
        if (cell.length == 0 && count > 0){
            if(vert) {x += 1; y = 0}
            else {y += 1; x = 0;}
            cell = $(".x"+x+"y"+y+"");
        }
        if(cell.length > 0 && !cell.hasClass("black"))
            select_cell(cell);
    }while(cell.length > 0 && cell.hasClass("black"))
}
function is_letter(keycode){
    return keycode >= 65 && keycode <= 90;
}

function highlight(cell){
    cell = $(cell);
    var vert = cell.parents("table").hasClass("vert");

    var vertClass = vert ? "primary" : "secondary";
    var horzClass = !vert ? "primary" : "secondary";

    var x = parseInt(cell.attr("x"));
    var y = parseInt(cell.attr("y"));

    var count = 0;
    var n = true;
    var s = true;
    var e = true;
    var w = true;

    while ((n || s || e || w) && count < 1000){
        if(n){
            var ele = $(".x"+x+"y"+(y-count));
            if (ele.length == 0 || ele.hasClass("black")){
                n = false;
            }
            else{
                ele.addClass(vertClass);
            }
        }
        if(s){
            var ele = $(".x"+x+"y"+(y+count));
            if (ele.length == 0 || ele.hasClass("black")){
                s = false;
            }
            else{
                ele.addClass(vertClass);
            }
        }
        if(e){
            var ele = $(".x"+(x+count)+"y"+y);
            if (ele.length == 0 || ele.hasClass("black")){
                e = false;
            }
            else{
                ele.addClass(horzClass);
            }
        }
        if(w){
            var ele = $(".x"+(x-count)+"y"+y);
            if (ele.length == 0 || ele.hasClass("black")){
                w = false;
            }
            else{
                ele.addClass(horzClass);
            }
        }
        count++;
    }
    show_clues();
}

function show_clues(){
    var vert = $(".crossword").hasClass("vert");
    var p_clue = parseInt($(".primary .clue").first().text());
    var s_clue = parseInt($(".secondary .clue").first().text());

    var p_index = vert ? 1 : 0;
    var s_index = vert ? 0 : 1;

    $("div.clue.primary").text(p_clue + ". " + clues[p_index][p_clue])
    $("div.clue.secondary").text(s_clue + ". " + clues[s_index][s_clue])
}
