from pprint import pprint
from http_lib import Request


def app(environ, start_response):
    request = Request(environ)
    pprint(environ)
    print(request.method)
    pprint(request.headers)
    pprint(request.query)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello from ... ']
