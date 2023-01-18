$(".activity-text-box")

		.keyup(async ( event ) => {
		    const payload = JSON.stringify({
			        name: event.target.value,
			    });
			console.log(payload)
		    const data = await fetch("http://127.0.0.1/api/save-activity", {
			    method: 'POST',
			    header: {'Content-Type': 'application/json'},
			    body: payload,
			})
			console.log(data)
		})
function loginPageRedirect(){
    window.location.href = "http://127.0.0.1/login"
}
function signInPageRedirect(){
    window.location.href = "http://127.0.0.1/sign-in"
}