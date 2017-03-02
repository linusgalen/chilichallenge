
$(document).ready(function () {
    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();

    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

        var $target = $(e.target);

        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);

    });
    $(".prev-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });

    $('input[type=radio][name=product_radio]').change(function() {
        // console.log(this.value);
        $('#next1_button').show();
    });

    //  $("#shipping_address_form :input").change(function() {
    //    $("#myform").data("changed",true);
    //    console.log('hej');
    //});

    $('#checkout_from').change(function(){
        // console.log($('#checkout_from').serializeArray());
        $('#checkout_from').v

        var $inputs = $('#checkout_from :input');

        // not sure if you wanted this, but I thought I'd add it.
        // get an associative array of just the values.
        var values = {};
        $inputs.each(function() {
            values[this.name] = $(this).val();
        });

        values['product_radio']=$("input[type='radio'][name=product_radio]:checked").val();
        var product_id=values['product_radio'];
        values['product_price']=$('#product_price_'+product_id).text();
        values['product_img']=$('#product_img_'+product_id).attr('src');
        values['product_description']=$('#product_description_'+product_id).text();

        $('#order_note').clearData();

        $('#order_note').append(values['product_price']);

        console.log(values);
    });



});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}