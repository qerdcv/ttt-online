from aiohttp import web
from src.routes import routes


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app


def main():
    app = create_app()
    web.run_app(host='0.0.0.0', port=8000, app=app)


if __name__ == '__main__':
    main()
