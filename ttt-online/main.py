import logging

from aiohttp import web

from src.config import Config
from src.app import create_app


def main():
    app = create_app()
    logging.info(Config.http_port)
    web.run_app(port=Config.http_port, app=app)


if __name__ == '__main__':
    main()
