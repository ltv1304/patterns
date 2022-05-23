from jinja2 import Environment, FileSystemLoader


class View:
    def __call__(self, request):
        http_method = request.method.lower()
        if hasattr(self, http_method):
            return getattr(self, http_method)(request)
        else:
            print('Выкинуть ошибку')

    @staticmethod
    def render(template_name, context={}):
        file_loader = FileSystemLoader('template')
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        return template.render(context=context)