from tortoise import fields, Model


class Profile(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    name = fields.CharField(max_length=50)
    age = fields.IntField()
    info = fields.TextField(null=True)
    offset = fields.IntField(default=0)
    telegram_id = fields.CharField(max_length=200, null=True)

    class Meta:
        table = "profiles"

    def __str__(self):
        return self.name
