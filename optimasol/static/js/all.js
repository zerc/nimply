(function ($) {
    /*
     * Do needed things about show/hide comments.
     */
    function init_comments() {
        var controls = $('span.hll');

        controls.click(function (e) {
            var control = $(this),
                comments = control.next('.comments');

            comments.toggleClass('hidden');
        });
    }

    init_comments();

}(jQuery));
