$(document).ready(function () {

    $('#confirm_code').validate({ // initialize the plugin
        rules: {
            generated_code: {
                required: true,
                email: true
            },
            order: {
                required: true,
                minlength: 5
            }
        },
        submitHandler: function (form) { // for demo
            alert('valid form submitted'); // for demo
            return false; // for demo
        }
    });

});