from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from originblog.extensions import mail


# def send_mail(subject, to, html):
#     message = Message(subject, recipients=[to], body=html)
#     mail.send_message(message)
# 创建异步发送邮件函数
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_async_mail(subject, to, html):
    app = current_app._get_current_object()  # 获取被代理的真实对象
    message = Message(subject, recipients=[to], body=html)
    thr = Thread(target=_send_async_mail, args=(app, message))
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_async_mail(subject='New Comment', to=current_app.config['ORIGINLOG_ADMIN_EMAIL'],
                    html=f'<p>New comment in post <i>{post.title}<i>, click the link below to check:</p>'
                    f'<p><a href="{post_url}">{post_url}</a></p>'
                    '<p><small style="color:#868e96">Do not reply this email.</small></p>')


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_async_mail(subject='New Reply', to=comment.email,
                    html=f'<p>New reply for the comment you left in post <i>{comment.post.id}<i>, click the link below to check:</p>'
                    f'<p><a href="{post_url}">{post_url}</a></p>'
                    '<p><small style="color:#868e96">Do not reply this email.</small></p>')
