$(".text-box")

		.keyup(async ( event ) => {
		    const payload = JSON.stringify({
			        name: event.target.value,
			    });
			console.log(payload)
		    const data = await fetch("http://192.168.68.108/api/saveactivity", {
			    method: 'POST',
			    header: {'Content-Type': 'application/json'},
			    body: payload,
			})
			console.log(data)
		})


