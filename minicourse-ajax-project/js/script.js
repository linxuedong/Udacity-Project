
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
    var $street = $('#street');
    var $city = $('#city');
    url = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=' +
        $street.val() + ', ' + $city.val();
    $body.append('<img src="' + url + '" alt="street view">')

    return false;
};

$('#form-container').submit(loadData);
