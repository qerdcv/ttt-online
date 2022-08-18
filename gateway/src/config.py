import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
    days = int(os.environ['COOKIE_AGE_DAYS'])
    cookie_name: str = os.environ['COOKIE_NAME']
    http_port: int = int(os.environ['HTTP_PORT'])
    profiler_url: str = os.environ['PROFILER_URL']

    @property
    def cookie_age(self) -> int:
        return self.days * 24 * 3600
