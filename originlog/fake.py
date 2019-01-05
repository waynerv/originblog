import random
from originlog.models import Admin, Post, Category, Comment, Link
from originlog.extensions import db
from faker import Faker

fake = Faker('zh_CN')


def fake_admin():
    admin = Admin(
        username='admin',
        name='kaka4nerv',
        blog_title='Originlog',
        blog_sub_title='Where everything begins...',
        about='Hello guys.'
    )
    admin.set_password('123456789')
    db.session.add(admin)
    db.session.commit()


def fake_post(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year(),
            category_id=random.randint(1, Category.query.count())
        )
        db.session.add(post)
    db.session.commit()


def fake_category(count=10):

    category = Category(name='default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def fake_link(count=4):
    for i in range(count):
        link = Link(name=fake.domain_name(), url=fake.url())
        db.session.add(link)
        db.session.commit()


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

    salt = int(count*0.1)
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
