$(document).ready(function () {
  $('#loginForm').submit(function (e) {
    e.preventDefault();

    const email = $('#email').val();
    const password = $('#password').val();

    $.ajax({
      url: 'php/login.php',
      method: 'POST',
      dataType: 'json', // expecting JSON
      data: {
        email: email,
        password: password
      },
      success: function (response) {
        if (response.status === 'success') {
          // Save login info to localStorage
          localStorage.setItem("loggedInUser", email);
          window.location.href = "profile.html"; // Redirect to profile
        } else {
          showError(response.message || "Invalid credentials");
        }
      },
      error: function (xhr, status, error) {
        showError("Something went wrong: " + error);
      }
    });
  });

  function showError(message) {
    $('#error').text(message).show();
  }
});
