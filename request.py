class Request:
    def __init__(self, environ):
        self.method = environ['REQUEST_METHOD']

        self.headers = self._get_headers(environ)
        self.queryes = self._get_query_string(environ['QUERY_STRING'])

    @staticmethod
    def _get_headers(environ: dict):
        headers = {}
        for key, val in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].lower()] = val
        return headers

    @staticmethod
    def _get_query_string(query_string: str):
        queries = {}
        if not len(query_string):
            return queries
        query_list = query_string.split('&')
        for item in query_list:
            key, val = item.split('=')
            queries[key] = val
        return queries
