from schematics.models import Model
from schematics.types import StringType, BooleanType
from schematics.exceptions import ValidationError


class Room(Model):
    room_name = StringType(required=True)
    is_private = BooleanType(default=False, required=True)
    password = StringType(default='')

    def validate_room_name(self, data, value):
        if len(data['room_name']) < 3:
            raise ValidationError('Too short')
        elif len(data['room_name']) > 27:
            raise ValidationError('Too long')
        return value

    def validate_password(self, data, value):
        if data['is_private'] is True and len(data['password']) <= 3:
            raise ValidationError('Too short')
        return value
