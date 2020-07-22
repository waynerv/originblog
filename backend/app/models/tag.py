from tortoise import Model, fields


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(32, unique=True)

    class Meta:
        table = 'tag'
