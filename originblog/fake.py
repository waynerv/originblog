import random

from faker import Faker

from originblog.models import User, Post, Comment, Widget, Role

fake = Faker('zh_CN')


def fake_admin():
    user = User(username='admin',
                name='waynerv',
                email='test@email.com',
                role='admin',
                bio='Hello guys.')
    user.set_password('123456789')
    user.role = Role.objects.filter(role_name='admin').first()
    user.save()


def fake_post(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            abstract=fake.sentence(30),
            author=User.objects.first(),
            raw_content=fake.text(2000),
            pub_time=fake.date_time_this_year(),
            tags=fake.words()
        )
        post.save()


def fake_widget(count=4):
    for i in range(count):
        widget = Widget(title=fake.word(), raw_content=fake.sentence())
        widget.save()


def fake_comment(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            homepage=fake.url(),
            md_content=fake.sentence(),
            status='approved',
            pub_time=fake.date_time_this_year(),
            post_slug=random.choice(Post.objects.distinct('slug'))
        )
        comment.save()

    salt = int(count * 0.1)
    # pending
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            homepage=fake.url(),
            md_content=fake.sentence(),
            status='pending',
            pub_time=fake.date_time_this_year(),
            post_slug=random.choice(Post.objects.distinct('slug'))
        )
        comment.save()

    # From author
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            homepage=fake.url(),
            md_content=fake.sentence(),
            status='approved',
            from_post_author=True,
            pub_time=fake.date_time_this_year(),
            post_slug=random.choice(Post.objects.distinct('slug'))
        )
        comment.save()

    # Reply
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            homepage=fake.url(),
            md_content=fake.sentence(),
            status='approved',
            pub_time=fake.date_time_this_year(),
            post_slug=random.choice(Post.objects.distinct('slug')),
            reply_to=random.choice(Comment.objects)
        )
        comment.save()
