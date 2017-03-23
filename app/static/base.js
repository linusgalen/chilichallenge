


$(document).ready(function() {

    $('body').scrollspy({target: ".navbar-me", offset: 50});

    $("#thenavbar a").on('click', function (event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function () {
                window.location.hash = hash;
            });
        }
    });

    /*$("#loginUsername").change(function(){
        $.ajax({
            method: "POST",
            url: "/usernameCheck",
            data:$("loginUsername").val()
        }).done(function( msg ) {
            alert( "Data Saved: " + msg );
        });
    });*/
});


$(window).scroll(function() {
    if($(this).scrollTop()>50) {
        $( ".navbar-me" ).addClass("fixed-me");
    } else {
        $( ".navbar-me" ).removeClass("fixed-me");
    }
});


