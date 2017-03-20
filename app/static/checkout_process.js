
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

    $('input[type=radio][name=product_radio]').change(function(e) {
        var selected_product=$("input[type='radio'][name=product_radio]:checked").val();
        $( "#stripe2" ).empty();
        $.ajax({
            type: "POST",
            url: 'loadprice',
            data: JSON.stringify(selected_product),
            //success: success,
            contentType: "application/json"
           // dataType: 'json'
        }).done(function( html ) {
            $( "#stripe2" ).append( html );
        });


        $('#next1_button').show();
    });



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
        values['product_name']=$('#product_name_'+product_id).text();


        $('#confirm_product_img').empty();
        $('#confirm_product_price').empty();
        $('#confirm_product_name').empty();
        $('#confirm_address').empty();
        $('#confirm_city').empty();
        $('#confirm_zipcode').empty();



        $('#confirm_product_img').append(values['product_img']);
        $('#confirm_product_price').append(values['product_price']);
        $('#confirm_product_name').append(values['product_name']);
        $('#confirm_address').append(values['address']);
        $('#confirm_zipcode').append(values['zipcode']);
        $('#confirm_city').append(values['city']);


        $('#stripe_script').attr('data-amount', 50000);
        $('#stripe_script').attr('data-description', 'betalning');


    });



});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}