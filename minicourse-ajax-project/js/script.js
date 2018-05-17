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
    $body.append('<img src="' + streetViewUrl + '" alt="street view">')

    // NY time request
    var nyUrl = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
    nyUrl += '?' + $.param({
        'api-key': "72510bba800d4a77b45ea262a182225e",
        'q': address
    });
    console.log(nyUrl);
    $.ajax({
        url: nyUrl,
        method: 'GET',
    }).done(function(result) {
        console.log(result);
        $.getJSON("ajax/test.json", function(data) {

        })
    }).fail(function(err) {
        throw err;
    });

    return false;
};

$('#form-container').submit(loadData);
