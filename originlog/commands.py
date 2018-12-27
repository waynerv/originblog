import click
from originlog.extensions import db


def register_command(app):
    @app.cli.command()
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(post, category, comment):
        from originlog.fake import fake_admin, fake_category, fake_comment,fake_post

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_category(category)

        click.echo(f'Generating {post} posts...')
        fake_post(post)

        click.echo(f'Generating {comment} comments...')
        fake_comment(comment)

        click.echo('Done.')
