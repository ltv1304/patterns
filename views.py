from jinja2 import Environment, FileSystemLoader

from http_lib import HttpResponce


def render(template_name, context):
    file_loader = FileSystemLoader('template')
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    return template.render(context=context)


def index_view(request):
    if request.method == 'GET':
        return HttpResponce(render('index.html', context={'about_url': '/about'}), request)
    else:
        return


def about_view(request):
    if request.method == 'GET':
        return HttpResponce(render('about.html', context={'index_url': '/'}), request)
    else:
        return
