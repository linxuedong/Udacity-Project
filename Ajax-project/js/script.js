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
        'q': cityStr
    });

    // $.ajax({
    //     url: nytUrl,
    //     method: 'GET',
    // }).done(function(result) {
    //     var items = [];
    //     $.each(result.response.docs, function(key, val) {
    //         $nytElem.append("<li id='" + key + "'>" + val.snippet + "</li>");
    //     });
    // }).fail(function(err) {
    //     throw err;
    // });

    // getJSON
    $.getJSON(nytUrl, function(data) {
        var items = data.response.docs
        for (var i = 0; i < items.length; i++) {
            var articleTitle = items[i].headline.main;
            var articleLink = items[i].web_url;
            $nytElem.append('<li class="article__item"><a href="' + articleLink + '">' + articleTitle + '</a></li>')
        }
        console.log(data);
    }).error(function() {
        $nytHeaderElem.text("New York Time Article Could Not Be Loaded")
    })


    // Wikipedia API
    var wikiRequestTimeout = setTimeout(function() {
      $wikiElem.text("Failed to get wikipedia respurces");
    }, 8000);

    var wikiUrl = 'https://zh.wikipedia.org/w/api.php'
    $.ajax({
        url: wikiUrl,
        data: {
            action: 'opensearch',
            search: cityStr,
            format: 'json'
        },
        method: 'GET',
        dataType: 'jsonp',
        success: function(result) {
            for (var i = 0; i < result[1].length; i++) {
                articleUrl = result[3][i];
                articleTitle = result[1][i]
                $wikiElem.append(
                    '<li class="wikipedia__item">' +
                    '  <a href="' + articleUrl + '" target="_blank">' + articleTitle + '</a>' +
                    '</li>'
                );
            }

            clearTimeout(wikiRequestTimeout);
        },
    })

    return false;
};

$('#form-container').submit(loadData);
