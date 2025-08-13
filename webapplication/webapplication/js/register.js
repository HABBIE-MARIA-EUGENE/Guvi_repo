$(function() {
    const $email = $('#email');
    const $pwd = $('#password');
    const $btn = $('#registerBtn');
    const $msg = $('#msg');

    // On clicking register btn

    $btn.on('click',function () {
        // getting i/p values
        const email = $email.val();
        const pwd = $pwd.val();

        //validating mail
        if(!email || !email.includes('@')) {
            $msg.text('Enter valid email address').removeClass().addClass('text-danger');
            return;  // stopping hereitself before calling server yet
        }
        
        
        //AJAX POST to php endpoint Since there will be no reload

        //jQ by default sends form-encoded body, PHP can read it via $_POST.

        $.ajax( {
            url:'../php/register.php',
            method: 'POST',
            dataType:'json',
            data: { email: email, password: pwd}
        })



        .done(res => {
            // handling json resp from php
            if (res.status === 'ok') {
                $msg.text('Registered Succesfully,Now you can Login')
                .removeClass().addClass('text-success');
            }

            else {
                $msg.text(res.message || 'Registration failed')
                .removeClass().addClass('text-danger');
            }
        })
        


        .fail(xhr => {
            //server crash or network error
            const m = (xhr.responseJSON && xhr.responseJSON.message)
            ? xhr.responseJSON.message
            : 'Server error';
            $msg.text(m).removeClass().addClass('text-danger');
        })
            

        

    })
    
})