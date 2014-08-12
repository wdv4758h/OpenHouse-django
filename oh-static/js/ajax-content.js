// need jQuery
if (window.history && window.history.replaceState) {
    aj = function (link, content_id) {
        $(document).on('click', link, function () {
            var href = $(this)[0].href;
            $(content_id).load(href);
            window.history.replaceState(null, null, href);
            return false;
        });
    };

    aj('a.ajax', '#content');

    update_navbar = function (root, new_url) {
        $('#navbar').load(root + '/navbar/');
        window.history.replaceState(null, null, new_url);
    };
}
