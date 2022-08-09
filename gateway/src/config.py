import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
