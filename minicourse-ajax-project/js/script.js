function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview

    // YOUR CODE GOES HERE!

    // Google street view request
    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var address = streetStr + ', ' + cityStr;
    console.log(address);

    var streetViewUrl = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=' +
        address;
    $('body').attr({
        'style': 'background-image: url("' + streetViewUrl + '")'
    });

    // NY time request
    var nytUrl = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    nytUrl += '?' + $.param({
        'api-key': "72510bba800d4a77b45ea262a182225e",
        'q': address
    });

    $.ajax({
        url: nytUrl,
        method: 'GET',
    }).done(function(result) {
        var items = [];
        $.each(result.response.docs, function(key, val) {
            $nytElem.append("<li id='" + key + "'>" + val.snippet + "</li>");
        });
    }).fail(function(err) {
        throw err;
    });
    // getJSON
    $.getJSON(nytUrl, function(data) {
        var items = data.response.docs
        for (var i = 0; i < items.length; i++) {
          var articleTitle = items[i].headline.main;
          var articleLink = items[i].web_url;
          console.log(articleTitle);
          $nytElem.append('<li class="atricle__item"><a href="' + articleLink + '">' + articleTitle + '</a></li>')
        }
        console.log(data);
    })

    return false;
};

$('#form-container').submit(loadData);
