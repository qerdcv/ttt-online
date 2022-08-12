import os
import logging

from aiohttp import web

from src.app import create_app

log = logging.getLogger(__name__)


def main():
    app = create_app()
    port = int(os.environ['GATEWAY_PORT'])
    log.info(f'started gateway service on {port} port')
    web.run_app(host='localhost', port=port, app=app)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
