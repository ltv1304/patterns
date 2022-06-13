from jinja2 import Environment, FileSystemLoader

from Framework.exceptions import Http405Error


class View:
    def __call__(self, request):
        http_method = request.method.lower()
        if self.is_allowed(http_method):
            return getattr(self, http_method)(request)
        else:
            raise Http405Error(self)

    def is_allowed(self, method):
        if hasattr(self, method):
            return True
        else:
            return False

    @staticmethod
    def render(template_name, context={}):
        file_loader = FileSystemLoader('template')
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        return template.render(context=context).encode("utf-8")
