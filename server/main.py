from aiohttp import web

from src.app import create_app


def main():
    app = create_app()
    web.run_app(host='0.0.0.0', port=8000, app=app)


if __name__ == '__main__':
    main()
