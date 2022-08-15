import os

from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class Envs(Enum):
    PROD = 'prod'
    DEV = 'dev'


@dataclass
class DBConfig:
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    database = os.environ['DB_DATABASE']
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']


@dataclass
class Config:
    db: DBConfig = DBConfig

    env: Envs = Envs(os.environ['ENV'])
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
    http_port = int(os.environ['HTTP_PORT'])

    @property
    def is_prod(self) -> bool:
        return self.env == Envs.PROD

    @property
    def is_dev(self) -> bool:
        return self.env == Envs.DEV
