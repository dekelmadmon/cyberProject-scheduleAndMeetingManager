$(".text-box")

		.keyup(async () => {
			const data = await $.ajax("/")
			alert(data)
		})