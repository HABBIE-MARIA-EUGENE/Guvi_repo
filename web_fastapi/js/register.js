// Register form JavaScript with jQuery & AJAX

$(document).ready(function() {
    
    // API Configuration
    const API_BASE_URL = 'http://localhost:8000';
    
    // Form submission handler
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = {
            name: $('#name').val().trim(),
            email: $('#email').val().trim(),
            password: $('#password').val(),
            confirmPassword: $('#confirmPassword').val()
        };
        
        // Clear previous messages
        $('.message').remove();
        
        // Client-side validation
        if (!validateForm(formData)) {
            return;
        }
        
        // Show loading state
        showLoading(true);
        
        // AJAX call to FastAPI backend
        $.ajax({
            url: API_BASE_URL + '/auth/register',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: formData.name,
                email: formData.email,
                password: formData.password
            }),
            success: function(response) {
                showLoading(false);
                showMessage('Account created successfully! Redirecting to login...', 'success');
                
                // Clear form
                $('#registerForm')[0].reset();
                
                // Redirect to login page after 2 seconds
                setTimeout(function() {
                    window.location.href = 'login.html';
                }, 2000);
            },
            error: function(xhr, status, error) {
                showLoading(false);
                
                let errorMessage = 'Registration failed. Please try again.';
                
                // Handle specific error responses from FastAPI
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    if (typeof xhr.responseJSON.detail === 'string') {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (Array.isArray(xhr.responseJSON.detail)) {
                        // Handle validation errors
                        errorMessage = xhr.responseJSON.detail.map(err => err.msg).join(', ');
                    }
                }
                
                showMessage(errorMessage, 'error');
            }
        });
    });
    
    // Client-side form validation
    function validateForm(data) {
        // Name validation
        if (!data.name || data.name.length < 2) {
            showMessage('Name must be at least 2 characters long', 'error');
            $('#name').addClass('error');
            return false;
        }
        
        // Email validation
        if (!isValidEmail(data.email)) {
            showMessage('Please enter a valid email address', 'error');
            $('#email').addClass('error');
            return false;
        }
        
        // Password validation
        if (data.password.length < 6) {
            showMessage('Password must be at least 6 characters long', 'error');
            $('#password').addClass('error');
            return false;
        }
        
        // Password confirmation
        if (data.password !== data.confirmPassword) {
            showMessage('Passwords do not match', 'error');
            $('#confirmPassword').addClass('error');
            return false;
        }
        
        // Clear error states if validation passes
        $('.form-group input').removeClass('error');
        return true;
    }
    
    // Email validation helper
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Show/hide loading state
    function showLoading(isLoading) {
        const submitBtn = $('.btn-primary');
        
        if (isLoading) {
            submitBtn.addClass('loading').prop('disabled', true).text('Creating Account...');
        } else {
            submitBtn.removeClass('loading').prop('disabled', false).text('Create Account');
        }
    }
    
    // Display messages
    function showMessage(message, type) {
        // Remove existing messages
        $('.message').remove();
        
        // Create message element
        const messageHtml = `<div class="message ${type}">${message}</div>`;
        
        // Insert before form
        $(messageHtml).insertBefore('#registerForm');
        
        // Auto-hide error messages after 5 seconds
        if (type === 'error') {
            setTimeout(function() {
                $('.message.error').fadeOut();
            }, 5000);
        }
    }
    
    // Real-time input validation
    $('#name').on('blur', function() {
        const name = $(this).val().trim();
        if (name && name.length >= 2) {
            $(this).removeClass('error').addClass('success');
        }
    });
    
    $('#email').on('blur', function() {
        const email = $(this).val().trim();
        if (email && isValidEmail(email)) {
            $(this).removeClass('error').addClass('success');
        }
    });
    
    $('#password').on('input', function() {
        const password = $(this).val();
        if (password.length >= 6) {
            $(this).removeClass('error').addClass('success');
        } else {
            $(this).removeClass('success');
        }
        
        // Check confirm password if it has value
        const confirmPassword = $('#confirmPassword').val();
        if (confirmPassword) {
            if (password === confirmPassword) {
                $('#confirmPassword').removeClass('error').addClass('success');
            } else {
                $('#confirmPassword').removeClass('success').addClass('error');
            }
        }
    });
    
    $('#confirmPassword').on('input', function() {
        const password = $('#password').val();
        const confirmPassword = $(this).val();
        
        if (confirmPassword === password && password.length >= 6) {
            $(this).removeClass('error').addClass('success');
        } else {
            $(this).removeClass('success').addClass('error');
        }
    });
    
    // Clear input error state on focus
    $('.form-group input').on('focus', function() {
        $(this).removeClass('error');
    });
    
});