

$(document).ready(function() {
    // $("nav a, .scroll-arrow a").on('click', function (event) {
    //     if (this.hash !== "") {
    //         event.preventDefault();
    //         var hash = this.hash;
    //         $('html, body').animate({
    //             scrollTop: $(hash).offset().top
    //         }, 800, function () {
    //             window.location.hash = hash;
    //         });
    //     }
    // });

    $(".carousel").carousel({
    interval: 3000
    });

});
