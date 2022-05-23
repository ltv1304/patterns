from Framework.http_lib import Request
from urls import urls, front_controller


def app(request: Request):
    front_controller.create_tree(urls)
    controller = front_controller.get_controller(request.path)
    return controller(request)
