from pprint import pprint

from Framework.http_lib import RequestWSGIServer, get_request_obj
from web_app import app, logger_app, fake_response_app


def wsgi_app(environ, start_response):
    request = get_request_obj(environ)
    response = app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]


def wsgi_logger_app(environ, start_response):
    request = get_request_obj(environ)
    response = logger_app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]


def wsgi_fake_response_app(environ, start_response):
    request = get_request_obj(environ)
    response = fake_response_app(request)
    start_response(response.response_status[:-2], list(response.headers_raw.items()))
    return [response.body]