// Wait for the document to load
$(document).ready(function () {
    // Attach the submit event
    $("#registerForm").submit(function (e) {
        e.preventDefault();  

        // Get input values
        let email = $("#email").val();
        let password = $("#password").val(); 

        // AJAX call to PHP
        $.ajax({
            url: "php/register.php", 
            type: "POST",
            data: {
                email: email,
                password: password
            },
            success: function (res) {
                $("#response").html(`<div class='alert alert-success'>${res}</div>`);
                window.location.href = "login.html";
            },
            error: function () {
                $("#response").html(`<div class='alert alert-danger'>Something went wrong</div>`);
            }
        });
    });
});
