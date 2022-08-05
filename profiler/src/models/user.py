from schematics.models import Model
from schematics.types import StringType, UUIDType


class User(Model):
    uid = UUIDType(required=False, default=None)
    username = StringType(required=True, min_length=4, max_length=30)
    password = StringType(required=True, min_length=4, max_length=30)
