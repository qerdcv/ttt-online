from aiohttp import web

from src.app import create_app
from src.config import Config


def main():
    app = create_app()
    web.run_app(port=Config.http_port, app=app)


if __name__ == '__main__':
    main()
