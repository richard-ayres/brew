jQuery(function (jQuery) {
    var $ = jQuery,
        brew_url = ''

    // populate hop select
    jQuery.ajax(brew_url + '/hop').done(function (data) {
        $('select[name="all-hops"]').append(
            data['_embedded'].map(hop => $('<option>')
                                .attr('value', hop['name'])
                                .attr('data', JSON.stringify(hop))
                                .text(hop['name']))
        );
    });

    // populate fermentable select
    jQuery.ajax(brew_url + '/fermentable').done(function (data) {
        $('select[name="all-fermentables"]').append(
            data['_embedded'].map(fermentable => $('<option>')
                                        .attr('value', fermentable['name'])
                                        .attr('data', JSON.stringify(fermentable))
                                        .text(fermentable['name']))
        );
    });
});