import random
from originblog.models import User, Post, Comment, Widget
from originblog.extensions import db
from faker import Faker

fake = Faker('zh_CN')


def fake_admin():
    user = User(
        username='admin',
        name='kaka4nerv',
        role='admin',
        bio='Hello guys.'
    )
    user.set_password('123456789')
    user.save()


def fake_post(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            abstract=fake.sentence(),
            raw_content=fake.text(2000),
            pub_time=fake.date_time_this_year(),
            tags = fake.word()
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
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post_id=random.randint(1, Post.query.count())
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=False,
            timestamp=fake.date_time_this_year(),
            post_id=random.randint(1, Post.query.count())
        )
        db.session.add(comment)

    for i in range(salt):
        comment = Comment(
            author='kaka4nerv',
            email='ampedee@163.com',
            site='shallwecode.top',
            body=fake.sentence(),
            from_admin=True,
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post_id=random.randint(1, Post.query.count())
        )
        db.session.add(comment)
    db.session.commit()

    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post_id=random.randint(1, Post.query.count()),
            replied=Comment.query.get(random.randint(1, Comment.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
