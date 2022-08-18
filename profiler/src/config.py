import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DBConfig:
    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    database = os.environ['DB_DATABASE']
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']


@dataclass
class Config:
    db: DBConfig = DBConfig()
    secret: str = os.environ['SECRET']
    base_dir: Path = Path(os.getcwd())
    grpc_port: int = int(os.environ['GRPC_PORT'])
