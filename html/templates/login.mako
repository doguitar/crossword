<%def name="login()">
    <div class="jumbotron col-xs-4 col-xs-offset-4" style="text-align: center;">
        <form id="login" action="${base}login">
            <input type="text" id="display" name="display" placeholder="display name" />
            <input type="text" id="email" placeholder="email" />
            <input type="password" id="password" placeholder="password" />
            <input type="password" id="confirm" placeholder="confirm" />

            <input type="hidden" name="email" />
            <input type="hidden" name="password" />
            <input type="hidden" name="confirm" />

            <input type="hidden" name="r" value="${return_url}" />
            <input type="submit" value="Login" />
        </form>
    </div>
</%def>