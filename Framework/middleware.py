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


def middleware(AGENT_CLASS, *args):
    def decorator(function):
        def wrapper(*func_args):
            agent = AGENT_CLASS(function, *args)
            result = agent(*func_args)
            return result
        return wrapper
    return decorator
