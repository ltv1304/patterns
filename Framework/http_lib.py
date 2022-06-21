import abc
from urllib.parse import parse_qs, urlparse

from Framework.exceptions import Http500Error

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']


def get_request_obj(data):
    if type(data) == dict:
        return RequestWSGIServer(data)
    elif type(data) == bytes:
        return RequestTestServer(data)
    else:
        assert Http500Error


class Request(abc.ABC):

    @property
    @abc.abstractmethod
    def method(self):
        pass

    @property
    @abc.abstractmethod
    def headers(self):
        pass

    @property
    @abc.abstractmethod
    def query(self):
        pass

    @property
    @abc.abstractmethod
    def path(self):
        pass

    @property
    @abc.abstractmethod
    def data(self):
        pass

    @property
    @abc.abstractmethod
    def data_len(self):
        pass

    @property
    @abc.abstractmethod
    def proto(self):
        pass

class RequestWSGIServer(Request):
    def __init__(self, environ: dict):
        self.environ = environ

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD')

    @property
    def headers(self):
        headers = {}
        for key, val in self.environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].lower()] = val
        return headers

    @property
    def query(self):
        query_string = self.environ.get('QUERY_STRING')
        query = {}
        if not len(query_string):
            return query
        query_list = query_string.split('&')
        for item in query_list:
            key, val = item.split('=')
            query[key] = val
        return query

    @property
    def path(self):
        return self.environ.get('PATH_INFO')

    @property
    def data_len(self):
        len_str = self.environ.get('CONTENT_LENGTH')
        return int(len_str) if len_str else 0

    @property
    def data(self):
        if self.data_len:
            data = self.environ['wsgi.input'].read(self.data_len) if self.data_len > 0 else b''
            return data.decode(encoding='utf-8')

    @property
    def proto(self):
        proto = self.environ.get('SERVER_PROTOCOL') or 'HTTP/1.1'
        return proto


class RequestTestServer(Request):
    def __init__(self, request: bytearray):
        request_string = request.decode(encoding='utf-8')
        request_lines = ''.join((line + '\n') for line in request_string.splitlines())
        head, self._data = request_lines.split('\n\n', 1)

        request_head = head.splitlines()
        request_headline = request_head[0]
        request_rest = {key: val for key, val in [item.split(': ') for item in request_head[1:]]}
        self._headers = dict(x.split(': ', 1) for x in request_head[1:])
        self._method, self.uri, self._proto = request_headline.split(' ', 3)
        self._data_len = int(request_rest.get('Content-Length')) if request_rest.get('Content-Length') else 0

    @property
    def url(self):
        return urlparse(self.uri)

    @property
    def path(self):
        return self.url.path

    @property
    def query(self):
        return parse_qs(self.url.query)

    @property
    def data(self):
        return self._data

    @property
    def method(self):
        return self._method

    @property
    def headers(self):
        return self._headers

    @property
    def data_len(self):
        return self._data_len

    @property
    def proto(self):
        return self._proto


class HttpResponseBase(abc.ABC):
    def __init__(self, response_body, request, additional_headers={}):
        self.body = response_body
        self.request = request
        self.additional_headers = additional_headers
        self.headers_raw = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': str(len(self.body)),
            'Connection': 'close',
        }
        self.response_proto = self.request.proto

    @property
    def headers(self):
        headers_full = {**self.headers_raw, **self.additional_headers}
        return ''.join(['{}: {}\n'.format(k, v) for k, v in headers_full.items()])


class HttpResponse(HttpResponseBase):
    def __init__(self, *args, response_status='200 OK\n', **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        self.response_status = response_status


class HttpResponseRedirect(HttpResponseBase):
    def __init__(self, redirect_url='/', *args, **kwargs):
        super(HttpResponseRedirect, self).__init__(*args, **kwargs)
        self.additional_headers['Location'] = redirect_url
        self.response_status = '303 See Other\n'

