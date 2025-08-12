// BASIC SYNTAX //

$(selector).action()

$ = Calling jQ function in short hand
selector = assume it as an string , helps to get html elements
action() = jQ method or function to perfom over the selected elements

Example:
    <script>

        $(document).ready(function() {
            $('h1').text('Welcome to jQ');
        } )

    </script>

