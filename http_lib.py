from urllib.parse import parse_qs, urlparse


class Request:
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']

        self.headers = self._get_headers(environ)
        self.query = self._get_query_string(environ['QUERY_STRING'])

    @staticmethod
    def _get_headers(environ: dict):
        headers = {}
        for key, val in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].lower()] = val
        return headers

    @staticmethod
    def _get_query_string(query_string: str):
        query = {}
        if not len(query_string):
            return query
        query_list = query_string.split('&')
        for item in query_list:
            key, val = item.split('=')
            query[key] = val
        return query


class TestRequest:
    def __init__(self, request: bytearray):
        request_string = request.decode()
        request_lines = ''.join((line + '\n') for line in request_string.splitlines())
        head, self.body = request_lines.split('\n\n', 1)

        request_head = head.splitlines()
        request_headline = request_head[0]
        self.headers = dict(x.split(': ', 1) for x in request_head[1:])
        self.method, self.uri, self.proto = request_headline.split(' ', 3)

    @property
    def url(self):
        return urlparse(self.uri)

    @property
    def path(self):
        return self.url.path

    @property
    def query(self):
        return parse_qs(self.url.query)


class HttpResponce:
    def __init__(self, responce_body, request):
        self.request = request
        self.body = responce_body
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(self.body),
            'Connection': 'close',
        }
        self.response_headers_raw = ''.join(['{}: {}\n'.format(k, v) for k, v in response_headers.items()])
        self.response_proto = 'HTTP/1.1'
        self.response_status = '200'
        self.response_status_text = 'OK'
