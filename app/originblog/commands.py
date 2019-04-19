import click
from mongoengine import connect

from originblog.models import User, Role


def register_command(app):
    @app.cli.command()
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    @click.option('--widget', default=4, help='Quantity of widgets, default is 4')
    def forge(post, widget, comment):
        """生成测试用的管理员账户、文章、widget、评论。

        生成测试数据时将删除所有并重新创建数据库中的表
        """
        from originblog.fake import fake_admin, fake_comment, fake_post, fake_widget

        db = connect('originblog')
        db.drop_database('originblog')

        click.echo('Initializing roles and permissions.')
        Role.init()  # 初始化角色与权限

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Administrator username: admin  password:123456789')

        click.echo(f'Generating {widget} widgets...')
        fake_widget(widget)

        click.echo(f'Generating {post} posts...')
        fake_post(post)

        click.echo(f'Generating {comment} comments...')
        fake_comment(comment)

        click.echo('Done.')

    @app.cli.command()
    def initdb():
        """重置数据库，删除所有集合"""
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db = connect('originblog')
        db.drop_database('originblog')
        click.echo('Drop database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--email', prompt=True, help='The email used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='The password used to login.')
    def init(username, email, password):
        """创建超级管理员账户"""
        admin_role = Role.objects.filter(role_name='admin').first()
        admin = User.objects.filter(role=admin_role).first()
        if admin:
            click.echo('The administrator is already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating new Administrator...')
            admin = User(
                username=username,
                name='administrator',
                email=email
            )
            admin.set_password(password)
            admin.role = admin_role
            admin.email_confirmed = True
            admin.save()

        click.echo('Done.')
