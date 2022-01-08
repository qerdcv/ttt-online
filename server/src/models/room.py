from schematics.models import Model
from schematics.types import StringType, BooleanType
from schematics.exceptions import ValidationError


class Room(Model):
    room_name = StringType(required=True, min_length=4, max_length=27)
    is_private = BooleanType(default=False, required=True)
    password = StringType(default='')

    def validate_password(self, data, value):
        if data['is_private'] is True and len(data['password']) <= 4:
            raise ValidationError('Too short')
        return value
