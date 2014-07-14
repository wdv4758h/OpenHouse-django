function(modal) {
    $('form', modal.body).submit(function() {
        $.ajax({
            type: 'POST',
            url: this.action,
            data: $(this).serialize(),
            success: function (data) { modal.respond('update', data); }
        });
        modal.close();
        return false;
    });
}
