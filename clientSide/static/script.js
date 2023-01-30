$(() => {
    $(".activity-text-box")

            .keyup(async ( event ) => {
                const payload = JSON.stringify({
                        name: event.target.value,
                    });
                console.log(payload)
                const data = await fetch("/api/save-activity", {
                    method: 'POST',
                    header: {'Content-Type': 'application/json'},
                    body: payload,
                })
                console.log(data)
            })

    $("#submit-sign-in")
            .click(async (event) => {
                const payload = JSON.stringify({
                    username: $("#user-name-sign-in").val(),
                    password: $("#password-sign-in").val(),
                });
                console.log(payload)
                $.cookie("username", $("#user-name-sign-in").val())
                $.cookie("password", $("#password-sign-in").val())
                const data = await fetch('/api/sign-in-info', {
                    method: 'POST',
                    header: {'Content-Type': 'application/json'},
                    body: payload,
                })
            })
})

function loginPageRedirect(){
    window.location.href = "/login"
}
function signInPageRedirect(){
    window.location.href = "/sign-in"
}

function getValue(classname){
    return $(classname).value()
}
