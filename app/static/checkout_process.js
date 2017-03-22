
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


    function getCurrentProductId(){
        return product_id=$("input[type='radio'][name=product_radio]:checked").val();
    }


    function getAmount() {
        var productId=getCurrentProductId();
        return parseInt($('#product_price_'+productId).text().replace(/[^0-9\.]/g, ''), 10)*100;
    }


    function getFirstName(){
        return $('#checkout_first_name').val()
    }

    function getLastName(){
        return $('#checkout_last_name').val()
    }

    function getZip(){
        return $('#checkout_zip').val()
    }

    function getAddress(){
        return $('#checkout_address').val();
    }

    function getCity(){
        return $('#checkout_city').val();
    }

    function getMessage(){
        return $('#checkout_message').val();
    }

    //Stripe Handler
    var handler = StripeCheckout.configure({
        key: 'pk_test_Y2poyAHtZzOY2qOmdqvzvizu',
        image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
        locale: 'auto',
        token: function(token) {
            // You can access the token ID with `token.id`.
            // Get the token ID to your server-side code for use.


            //Function for create a hidden from that submits and sends data to server
            var util = {};
            util.post = function (url, fields) {
                var $form = $('<form>', {
                    action: url,
                    method: 'post'
                });
                $.each(fields, function (key, val) {
                    $('<input>').attr({
                        type: "hidden",
                        name: key,
                        value: val
                    }).appendTo($form);
                });
                $form.appendTo('body').submit();
            };

            //Excecute form submit
            util.post('/charge', {
                tokenId: token.id,
                email: token.email,
                productId: getCurrentProductId(),
                address: getAddress(),
                zip: getZip(),
                city: getCity(),
                firstName: getFirstName(),
                lastName: getLastName(),
                message: getMessage()
            });


            //  var jsonData=JSON.stringify({
            //     tokenId:token.id,
            //     email:token.email,
            //     productId:getCurrentProductId()
            // });

            //console.log(jsonData);

            // $.ajax({
            //     dataType: "json",
            //     contentType: 'application/json',
            //     method: "POST",
            //     url: "/charge",
            //     data: jsonData
            // })

        }
    });




    $('#customButton').click(function(e) {
        // Open Checkout with further options:
        handler.open({
            name: 'Stripe Betalning',
            description: 'Chilichallenge',
            allowRememberMe: false,
            currency:'SEK',
            amount:getAmount()
        });
        e.preventDefault();
    });




    $('input[type=radio][name=product_radio]').change(function(e) {

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
        values['product_price']=parseInt($('#product_price_'+product_id).text().replace(/[^0-9\.]/g, ''), 10);
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



    });





// Close Checkout on page navigation:
    window.addEventListener('popstate', function() {
        handler.close();
    });



});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}