$(document).ready(function(e){
    $(".input-check").keypress(function(e){
        $(this).siblings(".label-check").empty();
    });
});