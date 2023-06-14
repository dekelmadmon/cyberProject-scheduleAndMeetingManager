let SOAB = {
  week: 0,
};

$(async () => {
  $(document).ready(() => {
    // Function to get the value of a cookie by name
    function getCookie(name) {
      const value = "; " + document.cookie;
      const parts = value.split("; " + name + "=");
      if (parts.length === 2) {
        return parts.pop().split(";").shift();
      }
      return "";
    }

    function updateScheduleHeader() {
      // Get the email cookie
      const email = getCookie("email");

      // ... existing code ...

      $.ajax({
        url: "/update_schedule_dates",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Cookie: `email=${email}`, // Include the email cookie in the request headers
        },
        data: JSON.stringify({
          factor: parseFloat(7 * SOAB.week + 1),
        }),
        dataType: "json",
        success: function (response) {
          // ... remaining code ...
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    }

    function getValue(class_name) {
      return $(class_name).val();
    }

    updateScheduleHeader();

    $(".activity-text-box").on("keyup", async (event) => {
      const payload = JSON.stringify({
        name: event.target.value,
      });
      console.log(payload);
      try {
        const response = await fetch("/api/save-activity", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Cookie: document.cookie, // Include all cookies in the request headers
          },
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
          headers: { "Content-Type": "application/json" },
          body: payload,
        });
        if (response.ok) {
          mainPageRedirect();
        } else {
          console.log("Failed to sign in.");
          console.log(response);
          alert("Invalid credentials or user exists already");
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
          headers: { "Content-Type": "application/json" },
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

    $("#next").on("click", async (event) => {
      SOAB.week++;
      updateScheduleHeader();
    });

    $("#previous").on("click", async (event) => {
      SOAB.week--;
      updateScheduleHeader();
    });

    const requestButton = $(".button-secondary");
    requestButton.click(function () {
      const attendee = $("#attendee").val();
      const sender = Cookies.get("email");
      const date = $("#date").val(); // Get the value of the date from an input field
      // send the attendee's email address to the Flask server
      $.ajax({
        url: "/request-meeting",
        method: "POST",
        contentType: "application/json",
        headers: {
          Cookie: `email=${sender}`, // Include the email cookie in the request headers
        },
        data: JSON.stringify({ attendee: attendee, sender: sender, date: date }),
        success: function (data) {
          console.log(data);
        },
      });
    });
  });
});

function mainPageRedirect() {
  window.location.href = "/main";
}

function loginPageRedirect() {
  window.location.href = "/login-page";
}

function signInPageRedirect() {
  window.location.href = "/sign-in-page";
}
