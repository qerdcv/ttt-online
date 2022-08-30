import os

from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class Envs(Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


@dataclass
class DBConfig:
    username: str = os.environ['DB_USERNAME']
    password: str = os.environ['DB_PASSWORD']
    database: str = os.environ['DB_DATABASE']
    host: str = os.environ['DB_HOST']
    port: str = os.environ['DB_PORT']

    @property
    def uri(self) -> str:
        return f'postgres://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'


@dataclass
class Config:
    db: DBConfig = DBConfig()
    env: Envs = Envs(os.environ['ENV'])
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
    http_port: int = int(os.environ['HTTP_PORT'])

    @property
    def is_prod(self) -> bool:
        return self.env == Envs.PROD

    @property
    def is_dev(self) -> bool:
        return self.env == Envs.DEV
