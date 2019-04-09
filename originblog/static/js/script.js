$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    }
});

function patchRequest(e) {
    var $el = $(e.target);
    // var id = $el.data('id');

    $.ajax({
        type: 'PATCH',
        url: $el.data('href'),
        success: function (data) {
            location.reload();
            alert(data.message);
        },
        error: function (error) {
            alert(error.message)  // TODO: 注册统一回调函数
        }
    });
}

function deleteRequest(e) {
    var $el = $(e.target);
    // var id = $el.data('id');

    $.ajax({
        type: 'DELETE',
        url: $el.data('href'),
        success: function (data) {
            location.reload();
            alert(data.message);
        },
        error: function (error) {
            alert(error.message)  // TODO: 注册统一回调函数
        }
    });
}

$(document).on('click', '.patch-request', patchRequest.bind(this));
$(document).on('click', '.delete-request', deleteRequest.bind(this));