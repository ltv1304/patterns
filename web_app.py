from Framework.http_lib import Request
from Framework.middleware import middleware, CORS
from urls import front_controller


@middleware(CORS, {'http://localhost:63342': ['GET']})
def app(request: Request):
    controller = front_controller.get_controller(request.path)
    return controller(request)
