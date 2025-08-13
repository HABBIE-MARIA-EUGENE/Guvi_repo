$(function() {
    
    //cacheing dom elem. into var i.e for quick access
    const $email = $('#email');
    const $pwd = $('#password');
    const $btn = $('#loginBtn');
    const $msg = $('#msg');


    //fn to show msg to user
    //text = message string
    //ok = true means success - greentext ,false error-red text
    function showMsg (text, ok=false) {
        $msg.text(text)                            // to set the msg txt
        .removeClass('text-danger text-success')   // removes old cls & assings class based on ok
        .addClass(ok ? 'text-success': 'text-danger');
    }

    //while clicking on login btn
    $btn.on('click', function() {

        //gets trimmed val from i/p
        const email = $email.val().trim();
        const pwd = $pwd.val();

        // client side quick validation
        //server will do its own checks too

        //need to add validation part if email, if pwd


        //ajax req to login.php

        $.ajax({

            url:'../php/login.php',
            method: 'POST',
            dataType:'json',
            data: { email: email, password: pwd}

        })

        //when req is success
        .done(res => {

            //server returns stat ok session :... , userid:... for success
            if (res.status === 'ok') {
                //save redis sess key in browser locstorage (client side alone)
                localStorage.setItem('sessionId', res.session);

                //save userid -- need to check and update later

                 console.log('login.php response:', res);

                //show succ msg
                showMsg('Login success! Redirecting...', true);

                //should set time out so that user can see the message before redirecting wait time 0.5s
                setTimeout(() => {
                    window.location.href= 'profile.html';
                }, 500);

            } else {

                //when login fails it will show the server`s error msg
                showMsg(res.message || 'Login failed !');
            }
        })

        //if req fails (server down or php error or ntwrk prblm)
        .fail(xhr => {
            //Try to extract server msg, otherwise it showa generic error
            const m = (xhr.responseJSON && xhr.responseJSON.message)
                        ? xhr.responseJSON.message
                        : 'Server Error!';
            showMsg(m);

        });


    });


});