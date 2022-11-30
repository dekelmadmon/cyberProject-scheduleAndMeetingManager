$(".text-box")

		.keyup(async () => {
			const data = await fetch("/api/saveactivity", {
			    method: 'POST',
			    header: {'Content-Type': 'application/json'},
			    body: JSON.stringify({
			        name: $(this).value,
			    }),
			})
			alert(data)
		})
