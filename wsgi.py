from Framework.http_lib import RequestWSGIServer
from web_app import app, logger_app, fake_response_app


def wsgi_app(environ, start_response):
    request = RequestWSGIServer(environ)
    response = app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]


def wsgi_logger_app(environ, start_response):
    request = RequestWSGIServer(environ)
    response = logger_app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]


def wsgi_fake_response_app(environ, start_response):
    request = RequestWSGIServer(environ)
    response = fake_response_app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]