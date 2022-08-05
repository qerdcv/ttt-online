import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    db_uri: str = os.environ['DB_URI']
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
