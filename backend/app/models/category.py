from tortoise import Model, fields


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(32, unique=True)

    class Meta:
        table = 'category'
