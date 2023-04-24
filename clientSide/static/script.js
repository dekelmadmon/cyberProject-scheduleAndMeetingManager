let SOAB = {
  week: 0,
};

$(async () => {
  $(document).ready(() => {
    function updateScheduleHeader() {
      console.log('updateScheduleHeader function called');
      $('#schedule-header th').each(async (index, element) => {
        console.log('schedule header function called');
        try {
          const response = await $.post({
            url: '/update_schedule_dates',
            method: 'post',
            data: JSON.stringify({
              factor: parseFloat((index + 7 * (SOAB.week) + 1)),
            }),
            contentType: "application/json",
            dataType: 'json',
          });
          console.log(response);
          var data = response.data;
          $(element).text(data);
        } catch (error) {
          console.log('Error:', error);
        }
      });
    }

    $(".activity-text-box").on("keyup", async (event) => {
      const payload = JSON.stringify({
        name: event.target.value,
      });
      console.log(payload);
      try {
        const response = await fetch("/api/save-activity", {
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: payload,
        });
        if (response.ok) {
          console.log("Activity saved successfully.");
        } else {
          console.log("Failed to save activity.");
        }
      } catch (error) {
        console.log("Error:", error);
      }
    });

    $("#submit-sign-in").on("click", async (event) => {
      const payload = JSON.stringify({
        username: $("#username-sign-in").val(),
        email: $("#email-sign-in").val(),
        password: $("#password-sign-in").val(),
      });
      console.log(payload);
      Cookies.set("username", $("#username-sign-in").val());
      Cookies.set("email", $("#email-sign-in").val());
      Cookies.set("password", $("#password-sign-in").val());
      try {
        const response = await fetch("/api/sign-in", {
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: payload,
        });
        if (response.ok) {
          mainPageRedirect();
        } else {
          console.log("Failed to sign in.");
          console.log(response);
        }
      } catch (error) {
        console.log("Error:", error);
      }
    });

    $("#submit-login").on("click", async (event) => {
      const payload = {
        email: $("#email-login").val(),
        password: $("#password-login").val(),
      };
      console.log(payload);
      Cookies.set("password", $("#password-login").val());
      Cookies.set("email", $("#email-login").val());
      let response;
      try {
        response = await fetch("/api/login", {
          method: "POST",
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (response.ok) {
          mainPageRedirect();
        } else {
          console.log("Failed to login.");
        }
      } catch (error) {
        console.log("Error:", error);
        console.log("Response:", response);
      }
    });

    $('#next').on("click", async (event) => {
      SOAB.week++;
      updateScheduleHeader();
    });

    $('#previous').on("click", async (event) => {
      SOAB.week--;
      updateScheduleHeader();
    });

})
})
    function mainPageRedirect() {
      updateScheduleHeader();
      $(window).on('load', function () {
        updateScheduleHeader();
      });
      window.location.href = "/main";
    }

    function loginPageRedirect () {
        window.location.href = "/login-page";
    }

    function signInPageRedirect() {
        window.location.href = "/sign-in-page";
    }

    function getValue(class_name) {
        return $(class_name).val();
    }
