import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
    days = int(os.environ['COOKIE_AGE_DAYS'])
    cookie_name = os.environ['COOKIE_NAME']

    @property
    def cookie_age(self) -> int:
        return self.days * 24 * 3600
