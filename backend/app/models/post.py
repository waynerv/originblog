from tortoise import Model, fields

from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(255, unique=True)
    slug = fields.CharField(128, unique=True)
    summary = fields.CharField(255)
    content = fields.TextField()
    type = fields.IntField()
    is_draft = fields.BooleanField()
    can_comment = fields.BooleanField()
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="posts"
    )
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="posts"
    )
    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="posts", through="post_tag"
    )
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        table = 'post'
