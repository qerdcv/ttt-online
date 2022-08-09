import os

from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class Envs(Enum):
    PROD = 'prod'
    DEV = 'dev'


@dataclass
class Config:
    env: Envs = Envs(os.environ['ENV'])
    db_uri: str = os.environ['MONOLITH_DB_URI']
    secret: str = os.environ['SECRET']

    base_dir: Path = Path(os.getcwd())

    @property
    def is_prod(self) -> bool:
        return self.env == Envs.PROD

    @property
    def is_dev(self) -> bool:
        return self.env == Envs.DEV
