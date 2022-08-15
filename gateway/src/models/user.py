import typing as t
from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    uid: t.Optional[UUID] = None
    username: t.Optional[str] = None
    password: t.Optional[str] = None
