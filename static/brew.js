jQuery(function (jQuery) {
    var $ = jQuery,
        brew_url = ''

    // populate hop select
    jQuery.ajax(brew_url + '/hops').done(function (data) {
        $('select[name="all-hops"]').append(
            data.map(hop => $('<option>')
                                .attr('value', hop['name'])
                                .attr('data', JSON.stringify(data))
                                .text(hop['name']))
        );
    });

    // populate fermentable select
    jQuery.ajax(brew_url + '/fermentables').done(function (data) {
        $('select[name="all-fermentables"]').append(
            data.map(fermentable => $('<option>')
                                        .attr('value', fermentable['name'])
                                        .attr('data', JSON.stringify(data))
                                        .text(fermentable['name']))
        );
    });
});