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
                    username: $("#username-sign-in").val(),
                    password: $("#password-sign-in").val(),
                });
                console.log(payload)
                Cookies.set("username", $("#username-sign-in").val())
                Cookies.set("password", $("#password-sign-in").val())
                const data = await fetch('/api/sign-in', {
                    method: 'POST',
                    header: {'Content-Type': 'application/json'},
                    body: payload,
                })
                window.location.href = "/main"
            })


    $("#submit-login")

            .click(async (event) => {

                const payload = JSON.stringify({
                    username: $("#username-login").val(),
                    password: $("#password-login").val(),
                    email: $("#email-login").val(),
                });
                console.log(payload)
                Cookies.set("username", $("#username-login").val())
                Cookies.set("password", $("#password-login").val())
                Cookies.set("email", $("#email-login").val())
                const data = await fetch('/api/login', {
                    method: 'POST',
                    header: {'Content-Type': 'application/json'},
                    body: payload,
                })
                window.location.href = "/main"
            })
})
function loginPageRedirect(){
    window.location.href = "/login-page"
}
function signInPageRedirect(){
    window.location.href = "/sign-in-page"
}

function getValue(class_name){
    return $(class_name).value()
}
