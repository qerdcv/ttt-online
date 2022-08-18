import logging

from aiohttp import web

from src.app import create_app
from src.config import Config

log = logging.getLogger(__name__)


def main():
    app = create_app()
    log.info(f'started gateway service on {Config.http_port} port')
    web.run_app(host='0.0.0.0', port=Config.http_port, app=app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
