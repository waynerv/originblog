// 初始化moment库
$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});

// 用来显示不同类型弹窗
var flash =null;
function toast(body, category) {
    clearTimeout(flash);
    var $toast = $('#toast');
    if (category === 'error') {
        $toast.css('background-color', 'red') // 错误类型消息
    } else {
        $toast.css('background-color', '#333') // 普通类型消息
    }
    $toast.text(body).fadeIn();
    flash = setTimeout(function () {
        $toast.fadeOut();
    }, 3000)
}

// 通过jQuery的ajaxSetup()方法设置AJAX，添加CSRF令牌
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    }
});

// 通过jQuery的ajaxError()方法设置统一处理error回调函数
$(document).ajaxError(function (event, request, settings) {
    var message = null;
    if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
        message = request.responseJSON.message
    } else if (request.responseText) {
        var IS_JSON = true;
        try {
            var data = JSON.parse(request.responseText); // 作为JSON解析
        }
        catch(err) {
            IS_JSON = false
        }

        if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
            message = JSON.parse(request.responseText).message;
        } else {
            message = default_error_message; // 使用默认错误消息
        }
    } else {
        message = default_error_message; // 使用默认错误消息
    }
    toast(message, 'error'); // 弹出提示消息
});

// 发送PATCH方法ajax请求切换文章评论状态并更新页面
function switchComment(e) {
    var $el = $(e.target);

    $.ajax({
        type: 'PATCH',
        url: $el.data('href'),
        success: function (data) {
            if (data.message.includes('disabled')) {
                $el.text('Enable Comment');
            } else if (data.message.includes('enabled')) {
                $el.text('Disabled Comment');
            }
            toast(data.message);
        },
        // 使用统一回调函数
        // error: function (error) {
        //     alert(error.message)
        // }
    });
}

// 发送PATCH方法ajax请求审核评论并更新页面
function handleComment(e) {
    var $el = $(e.target);
    var id = $el.data('id');

    $.ajax({
        type: 'PATCH',
        url: $el.data('href'),
        data: JSON.stringify({'operation': $el.data('op')}),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            $('.'+id+'button').remove();
            if (data.message.includes('approved')) {
                $('#'+id+'status').text('approved');
            } else if (data.message.includes('Spam')) {
                $('#'+id+'status').text('spam');
            }
            toast(data.message);
        },
    });
}

// 发送DELETE方法ajax请求的通用函数
function deleteItem(e) {
    var $el = $(e.target);
    //注意下面不能直接使用jQuery的data()获取，因为同一元素通过data()获取的值不会改变
    var id = $el.attr('data-id');

    $.ajax({
        type: 'DELETE',
        url: $el.attr('data-href'),
        success: function (data) {
            $('#'+id).remove();
            toast(data.message);
        },
    });
}

// 发送DELETE方法ajax请求删除所有待审核评论
function deleteAll(e) {
    var $el = $(e.target);

    $.ajax({
        type: 'DELETE',
        url: $el.data('href'),
        success: function (data) {
            location.reload()
        },
    });
}

// 删除文章并跳转到首页
function deletePost(e) {
    var $el = $(e.target);

    $.ajax({
        type: 'DELETE',
        url: $el.data('href'),
        data: JSON.stringify({'flash': 'True'}),
        contentType: 'application/json; charset=UTF-8',
        success: function (data) {
            location.href = "/";
            return false;
        },
    });
}

// 绑定事件到按钮
$(document).on('click', '.switch-comment', switchComment.bind(this));
$(document).on('click', '.handle-comment', handleComment.bind(this));
$(document).on('click', '.delete-item', deleteItem.bind(this));
$(document).on('click', '.delete-all', deleteAll.bind(this));
$(document).on('click', '.delete-post', deletePost.bind(this));

// 多个删除按钮共用一个模态框
$('#confirm-delete').on('show.bs.modal', function (e) {
    $('.delete-item').attr('data-id', $(e.relatedTarget).data('id'));
    $('.delete-item').attr('data-href', $(e.relatedTarget).data('href'));
});

$('#delete-all').on('show.bs.modal', function (e) {
    $('.delete-all').attr('data-id', $(e.relatedTarget).data('id'));
    $('.delete-all').attr('data-href', $(e.relatedTarget).data('href'));
});

$('#delete-post').on('show.bs.modal', function (e) {
    $('.delete-post').attr('data-id', $(e.relatedTarget).data('id'));
    $('.delete-post').attr('data-href', $(e.relatedTarget).data('href'));
});

// 向文章正文中的图片和表格添加样式
$('#main-content img').addClass('img-fluid');
$('#main-content table').addClass('table table-bordered small');