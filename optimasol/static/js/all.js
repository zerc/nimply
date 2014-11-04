(function ($) {
    var add_comment_form = $('form[name="comment_add_form"]'),
        form_holder = add_comment_form.parent(),
        line_height = 22;

    /*
     * Init Form
     */

    add_comment_form.find('button[role="close"]').click(function (e) {
        form_holder.css('top', -9999);
        return false;
    });

    add_comment_form.find('button[role="submit"]').click(function (e) {
        var data = $('form[name="comment_add_form"]').serialize();
        $.post(
            add_comment_form.attr('action'),
            data,
            function (resp) {
                if (resp.status) {
                    location.reload();
                }
            }
        );
        return false;
    });


    /*
     * Do needed things about show/hide comments.
     */
    function init_comments() {
        var controls = $('span.hll'),
            lines = $('span[id*="line-"]');

        controls.click(function (e) {
            var control = $(this),
                comments = control.parent().next('.comments');

            if (comments.hasClass('hidden')) {
                comments.removeClass('hidden');
            } else {
                comments.addClass('hidden');
                e.stopPropagation();
                form_holder.css('top', -9999);
            }
        });

        lines.click(function (e) {
            var el = $(this),
                top = el.offset().top + line_height + (el.next('.comments').outerHeight() || 0);

            el.toggleClass('selected');
            form_holder.css('top', top);
            add_comment_form.find('input[name="line"]').val(
                el.attr('id').replace('line-', ''));
        });
    }

    init_comments();

}(jQuery));
