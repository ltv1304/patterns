from urls import *


def app(request):
    controller = front_controller.get_controller(request.path)
    return controller(request)