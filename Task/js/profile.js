$(document).ready(function () {
  const email = localStorage.getItem("loggedInUser");

  if (!email) {
    alert("No session found. Please login again.");
    window.location.href = "login.html";
    return;
  }

  // ✅ Load profile
  $.ajax({
    url: "php/check_session.php",
    type: "POST",
    data: { email: email },
    success: function (response) {
      if (response.status === "success") {
        $("#email").val(email);
        $("#age").val(response.profile.age);
        $("#dob").val(response.profile.dob);
        $("#contact").val(response.profile.contact);
      } else {
        alert(response.message || "Session verification failed.");
        window.location.href = "login.html";
      }
    },
    error: function (xhr) {
      console.error(xhr.responseText);
      alert("Server error. Please try again.");
    }
  });

  // ✅ Update profile
  $("#profileForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
      url: "php/update_profile.php",
      type: "POST",
      data: {
        email: email,
        age: $("#age").val(),
        dob: $("#dob").val(),
        contact: $("#contact").val()
      },
      success: function (response) {
        const res = typeof response === "string" ? JSON.parse(response) : response;
        if (res.status === "success") {
          $("#message").text(res.message).show();
        } else {
          alert(res.message);
        }
      },
      error: function (xhr) {
        console.error(xhr.responseText);
        alert("Failed to update profile.");
      }
    });
  });

  // ✅ Logout
  $("#logoutBtn").click(function () {
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
  });
});
