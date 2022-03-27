from schematics.models import Model
from schematics.types import IntType


class Paginator(Model):
    page = IntType(default=1)
    limit = IntType(default=10, max_value=100)
