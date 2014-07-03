/* Header search behaviour */
if(window.headerSearch){
    var search_current_index = 0;
    var search_next_index = 0;

    $(window.headerSearch.termInput).on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 200);
        $(this).data('timer', wait);
    });

    // auto focus on search box
    $(window.headerSearch.termInput).trigger('focus');

    function search () {
        var workingClasses = "icon-spinner";

        $(window.headerSearch.termInput).parent().addClass(workingClasses);
        search_next_index++;
        var index = search_next_index;
        $.ajax({
            url: window.headerSearch.url,
            data: {q: $(window.headerSearch.termInput).val()},
            success: function(data, status) {
                if (index > search_current_index) {
                    search_current_index = index;
                    $(window.headerSearch.targetOutput).html(data).slideDown(800);
                    window.history.pushState(null, "Search results", "?q=" + $(window.headerSearch.termInput).val());
                }
            },
            complete: function(){
                $(window.headerSearch.termInput).parent().removeClass(workingClasses);
            }
        });
    }
}
