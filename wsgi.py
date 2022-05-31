from Framework.http_lib import RequestWSGIServer
from web_app import app


def wsgi_app(environ, start_response):
    request = RequestWSGIServer(environ)
    response = app(request)
    start_response(response.response_status, list(response.headers_raw.items()))
    return [response.body.encode()]
