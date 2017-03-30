

$(function() {

    //Set up instafeed
    var Instafeed = require("Instafeed.js");
    var feed = new Instafeed({
        clientId: 'c1679b258e31400b977e8243af3b10d8',
        target: 'instafeed',
        get: 'popular',
        links: true,
        limit: 5,
        sortBy: 'most-recent',
        resolution: 'standard_resolution',
        template: '<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3"><div class="photo-box"><div class="image-wrap"><a href="{{link}}"><img src="{{image}}"></a><div class="likes">{{likes}} Likes</div></div><div class="description">{{caption}}<div class="date">{{model.date}}</div></div></div></div>'
    });
    feed.run();

});
