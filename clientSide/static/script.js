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
function loginPageRedirect(){
    window.location.href = "/login"
}
function signInPageRedirect(){
    window.location.href = "/sign-in"
}

function getValue(classname){
    return $(classname).val()
}
$(".submit-sign-in")
        .keyup(async (event) => {
            const payload = JSON.stringify({
            username: $(".user-name-sign-in").val(),
            password: $(".password-sign-in").val(),
            });
            console.log(payload)
            const data = await fetch('/api/sign-in-info', {
			    method: 'POST',
			    header: {'Content-Type': 'application/json'},
			    body: payload,
			})
        })