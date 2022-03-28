import json
import math
import typing as t
from dataclasses import dataclass


@dataclass
class Paginator:
    page: int = 1
    limit: int = 10

    def create_paginator(self, page: t.Optional[str], limit: t.Optional[str]):
        if page is not None:
            self.page = math.floor(json.loads(page))
        if limit is not None:
            limit = math.floor(json.loads(limit))
            if limit > 100:
                self.limit = 100
            elif limit > 0:
                self.limit = limit
