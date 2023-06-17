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
      $.ajaxSetup({
        xhrFields: {
          withCredentials: true, // Include cookies in the request
        },
      });

      $.ajax({
        url: "/update_schedule_dates",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
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
      const date = $("#date").val(); // Get the value of the date from an input field
      // send the attendee's email address to the Flask server
      $.ajax({
        url: "/request-meeting",
        method: "POST",
        contentType: "application/json",

        data: JSON.stringify({ attendee: attendee, date: date }),
        success: function (data) {
          console.log(data);
        },
      });
    });

    const recieveMeetings = $(".button-recieve-meetings");
    recieveMeetings.on("click", async (event) => {
      let response;
    fetch("/recieve-meetings", {
      method: "GET"
    })
      .then(response => {
        if (response.ok) {
          // Check if the response was successful (status code in the range of 200-299)
          // For JSON response:
          return response.json(); // Returns a promise that resolves to the parsed JSON data
          // For other response types:
          // return response.text(); // Returns a promise that resolves to the response text
          // return response.blob(); // Returns a promise that resolves to a Blob object
        } else {
          throw new Error("Request failed with status code " + response.status);
        }
      })
      .then(data => {
        // Process the retrieved data
        console.log(data);
        populateMeetingsTable(data)
      })
      .catch(error => {
        console.error(error);
      });
    });

  });
});

function populateMeetingsTable(jsonData) {
    debugger;
    // Parse the JSON data
    const data = JSON.parse(JSON.stringify(jsonData));

    // Create the HTML table structure
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    // Generate table header based on the keys of the JSON object
    const headers = Object.keys(data[0]);
    const headerRow = document.createElement("tr");
    headers.forEach(header => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Generate table rows and cells based on the values of each key
    data.forEach(item => {
      const row = document.createElement("tr");
      headers.forEach(header => {
        const cell = document.createElement("td");
        cell.textContent = item[header];
        row.appendChild(cell);
      });
      tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Append the table to the container element in the HTML document
    const tableContainer = document.getElementById("table-container");
    tableContainer.appendChild(table);
}

function mainPageRedirect() {
  window.location.href = "/main";
}

function loginPageRedirect() {
  window.location.href = "/login-page";
}

function signInPageRedirect() {
  window.location.href = "/sign-in-page";
}
function acceptMeeting() {
    alert(`Meeting request accepted from ${sender} at ${date}`);
}

// Function to handle meeting decline
function declineMeeting() {
    alert(`Meeting request declined from ${sender} at ${date}`);
}