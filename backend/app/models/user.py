from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(64, unique=True, description='邮箱地址')
    name = fields.CharField(64, description='姓名')
    password_hash = fields.CharField(128, description='密码哈希值')
    avatar = fields.CharField(128, null=True, description='头像地址')

    class Meta:
        table = 'user'
