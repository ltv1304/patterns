import datetime
import time

from Framework.http_lib import HttpResponse
from urllib.parse import urlparse


class CORS:
    def __init__(self, get_response, allowed_origins):
        self._get_response = get_response
        self._allowed_origins = allowed_origins

    def __call__(self, request):
        if self.cors_request(request.headers):
            if request.headers['Origin'] in self._allowed_origins:
                return self.get_cors_response(request)
            else:
                return HttpResponse('', request)
        else:
            response = self._get_response(request)
        return response

    def get_cors_response(self, request):
        if request.method == 'OPTIONS':
            allowed_methods = self._allowed_origins[request.headers['Origin']]
            header = {
                'Access-Control-Allow-Methods': ' '.join(allowed_methods),
                'Access-Control-Allow-Origin': request.headers['Origin'],
                'Access-Control-Allow-Headers': '*',
            }
            return HttpResponse('', request, header)
        else:
            response = self._get_response(request)
            response.additional_headers = {
                'Access-Control-Allow-Origin': request.headers['Origin'],
                'Access-Control-Allow-Headers': '*',
            }
            return response

    @staticmethod
    def cors_request(headers):
        if headers.get('Origin'):
            if headers.get('Host') != urlparse(headers['Origin']).netloc:
                return True
        return False


class AppLogger:
    def __init__(self, get_response, name):
        self._get_response = get_response
        self.name = name

    def __call__(self, request):
        print(f'{self.name}: [{request.method}] on {request.path}')
        return self._get_response(request)


class FakeResponse:
    def __init__(self, get_response, response_status):
        self._get_response = get_response
        self.response_status = response_status

    def __call__(self, request):
        response = HttpResponse(''.encode(), request)
        response.response_status = self.response_status
        return response


def middleware(AGENT_CLASS, *args):
    def decorator(function):
        def wrapper(*func_args):
            agent = AGENT_CLASS(function, *args)
            result = agent(*func_args)
            return result
        return wrapper
    return decorator


def debug(logger_name):
    def decorator(cls):
        class Logger:
            def __init__(self, *args, **kwargs):
                self.name = logger_name
                self._obj = cls(*args, **kwargs)

            def __call__(self, request):
                print(f'From {self.name} logger: {datetime.datetime.now()} called method {request.method} of class {type(self._obj).__name__}')
                return self._obj.__call__(request)

        return Logger
    return decorator
