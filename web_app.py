from Framework.http_lib import Request
from Framework.middleware import middleware, CORS, AppLogger, FakeResponse
from urls import front_controller


@middleware(CORS, {'http://localhost:63342': ['GET']})
def app(request: Request):
    controller = front_controller.get_controller(request.path)
    return controller(request)


@middleware(AppLogger, 'app logger')
def logger_app(request: Request):
    return app(request)


@middleware(FakeResponse, '200 OK')
def fake_response_app(request: Request):
    return app(request)
