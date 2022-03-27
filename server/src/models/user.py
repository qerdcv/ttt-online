from schematics.models import Model
from schematics.types import IntType, StringType


class User(Model):
    id = IntType(required=False, default=None)
    username = StringType(required=True, min_length=4, max_length=30)
    password = StringType(required=True, min_length=4, max_length=30)

