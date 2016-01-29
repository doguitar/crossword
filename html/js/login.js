$(document).ready(function(){
    $("#login").on('submit', function(e) {
        var action = this.action;

        var display = $("#display").val();
        var email = hash($("#email").val());
        var password = hash($("#password").val());
        var confirm = hash($("#confirm").val());

        if($("#go").val()=="1") {
            $("input[name='email']").val(email);
            $("input[name='password']").val(password);
            $("input[name='confirm']").val(confirm);
            return true;
        }
        $.get(action, {email : email})
            .success(function(data) {
                if (data === "exists") {
                    $.get(action, {email: email, password: password})
                        .success(function (data) {
                            if(data){
                                $("#login").append("<input id='go'  type='hidden' value='1' />");
                                $("#login").submit()
                            }
                            else{//invalid password

                            }
                        });
                }
                else if (data === "invalid"){//invalid email

                }
                else{//new
                    if (display.length > 0 && confirm.length > 0 && confirm === password) {
                        $("#login").append("<input id='go' type='hidden' value='1' />");
                        $("#login").submit()
                    }
                    else {
                        $("#confirm, #display").show();
                    }
                }
            });
        return false;
    });
});

function hash(string){
    return CryptoJS.SHA3(string).toString();
}