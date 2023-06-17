let SOAB = {
  week: 0,
};

var email;

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

    function updateEmail() {
      // Get the email cookie
      email = getCookie("email");
    }

    updateEmail();

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

    function fetchMeetings() {
      fetch("/recieve-meetings", {
        method: "GET"
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Request failed with status code " + response.status);
          }
        })
        .then(data => {
          console.log(data);
          populateMeetingsTable(data);
        })
        .catch(error => {
          console.error(error);
        });
    }

    // Check if the current page URL is main.html before executing the function
    if (window.location.pathname === "/main") {
      // Execute the function immediately
      fetchMeetings();

      // Execute the function every 10 seconds
      setInterval(fetchMeetings, 3000);
    }
  });
});

function populateMeetingsTable(jsonData) {
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
  // Add an extra column for buttons
    const th = document.createElement("th");
    th.textContent = "Actions";
    headerRow.appendChild(th);

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

    const requester = item["requester"]
    const reciever = item["reciever"]
    const date = item["date"]
    const status = item["status"]

    // Add buttons based on conditions
    const actionsCell = document.createElement("td");
    if (status === "Canceled") {
        actionsCell.innerHTML = "-";
    } else if (requester === email) {
      // Requester is the client, add cancel button
      const cancelButton = document.createElement("button");
      cancelButton.textContent = "Cancel";
      cancelButton.addEventListener("click", () => {
          // send the attendee's email address to the Flask server
          $.ajax({
            url: "/update-meeting",
            method: "POST",
            contentType: "application/json",

            data: JSON.stringify({ requester: requester, attendee: reciever, date: date, status: "Canceled" }),
            success: function (data) {
              console.log(data);
            },
          });
        });
      actionsCell.appendChild(cancelButton);
    } else {
      // Recipient is the client, add approve and decline buttons
      const approveButton = document.createElement("button");
      approveButton.textContent = "Approve";
      approveButton.addEventListener("click", () => {
          // send the attendee's email address to the Flask server
          $.ajax({
            url: "/update-meeting",
            method: "POST",
            contentType: "application/json",

            data: JSON.stringify({ requester: requester, attendee: reciever, date: date, status: "Approved" }),
            success: function (data) {
              console.log(data);
            },
          });
        });
      actionsCell.appendChild(approveButton);

      const declineButton = document.createElement("button");
      declineButton.textContent = "Decline";
      declineButton.addEventListener("click", () => {
          // send the attendee's email address to the Flask server
          $.ajax({
            url: "/update-meeting",
            method: "POST",
            contentType: "application/json",

            data: JSON.stringify({ requester: requester, attendee: reciever, date: date, status: "Declined" }),
            success: function (data) {
              console.log(data);
            },
          });
        });
      actionsCell.appendChild(declineButton);
    }

    row.appendChild(actionsCell);
    tbody.appendChild(row);
  });
  table.appendChild(tbody);

  // Append the table to the container element in the HTML document
  const tableContainer = document.getElementById("table-container");
  tableContainer.innerHTML = "";
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