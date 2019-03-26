import click
from originblog.extensions import db
from originblog.models import Admin, Category


def register_command(app):
    @app.cli.command()
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    @click.option('--link', default=4, help='Quantity of links, default is 4')
    def forge(post, category, comment, link):
        """生成测试用的管理员账户、文章、分类、评论、以及链接。

        生成测试数据时将删除所有并重新创建数据库中的表
        :param post: 将要生成文章的数量
        :param category: 将要生成分类的数量
        :param comment: 将要生成评论的数量
        :param link: 将要生成链接的数量
        :return: None
        """
        from originblog.fake import fake_admin, fake_category, fake_comment, fake_post, fake_link

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_category(category)

        click.echo(f'Generating {link} links...')
        fake_link(link)

        click.echo(f'Generating {post} posts...')
        fake_post(post)

        click.echo(f'Generating {comment} comments...')
        fake_comment(comment)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--drop', is_flag=True)
    def initdb(drop):
        """重置数据库，删除所有表并重新创建

        :param drop: 是否删除表
        :return: None
        """
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized Database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='The password used to login.')
    def init(username, password):
        """建表并创建管理员账户以及初始文章类别

        :param username: 管理员用户名
        :param password: 管理员密码
        :return: None
        """
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('The administrator is already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating new Administrator...')
            admin = Admin(username=username, name='kaka4nerv', blog_title='Originlog',
                          blog_sub_title='Where everything begins...', about='Anything about you.')
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')
