import abc
from urllib.parse import parse_qs, urlparse


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']


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


class RequestTestServer(Request):
    def __init__(self, request: bytearray):
        request_string = request.decode(encoding='utf-8')
        request_lines = ''.join((line + '\n') for line in request_string.splitlines())
        head, self._data = request_lines.split('\n\n', 1)

        request_head = head.splitlines()
        request_headline = request_head[0]
        request_rest = {key: val for key, val in [item.split(': ') for item in request_head[1:]]}
        self._headers = dict(x.split(': ', 1) for x in request_head[1:])
        self._method, self.uri, self.proto = request_headline.split(' ', 3)
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


class HttpResponse:
    def __init__(self, responce_body, request, additional_headers={}):
        self.request = request
        self.body = responce_body
        self.headers_raw = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': str(len(self.body)),
            'Connection': 'close',
        }
        self.additional_headers = additional_headers
        self.response_proto = 'HTTP/1.1'
        self.response_status = '200 OK\n'

    @property
    def headers(self):
        headers_full = {**self.headers_raw, **self.additional_headers}
        return ''.join(['{}: {}\n'.format(k, v) for k, v in headers_full.items()])


class HttpResponseRedirect:
    def __init__(self, response_body, request):
        self.request = request
        self.body = response_body.encode("utf-8")
        self.headers_raw = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': str(len(self.body)),
            'Connection': 'close',
            'Location': '/success'
        }
        self.headers = ''.join(['{}: {}\n'.format(k, v) for k, v in self.headers_raw.items()])
        self.response_proto = 'HTTP/1.1'
        self.response_status = '303 See Other\n'

