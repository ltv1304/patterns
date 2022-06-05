from Framework.http_lib import HttpResponse, HttpResponseRedirect
from Framework.middleware import debug
from Framework.view import View
from model import CategoryFactory, Fabric

context = {
        'index': '/',
        'about': '/about',
        'contacts': '/contacts',
        'course': '/course',
        'category': '/category',
    }


@debug('test')
class IndexView(View):
    def get(self, request):
        return HttpResponse(self.render('index.html', context=context), request)


class AboutView(View):

    def get(self, request):
        return HttpResponse(self.render('about.html', context=context), request)


@debug('test1')
class ContactsView(View):

    def get(self, request):
        return HttpResponse(self.render('contacts.html', context=context), request)

    def post(self, request):
        if request.data_len:
            message = request.data
            print(message)
            message_fields = message.split('&')
            message_dict = {}
            for field in message_fields:
                key, val = field.split('=', 1)
                message_dict[key]=val
            print(f'Получено сообщение от пользователя: {message_dict["name"]}(e-mail: {message_dict["mail"]})')
            print(f'Текс сообщения:')
            print(message_dict["message"])
        return HttpResponseRedirect('', request)


class SuccessView(View):

    def get(self, request):
        return HttpResponse(self.render('success_page.html'), request)


class CourseView(View):
    course_list = []

    def get(self, request):
        context['courses'] = self.course_list
        context['categories'] = CategoryView.category_list
        return HttpResponse(self.render('course.html', context=context), request)

    def post(self, request):
        if request.data_len:
            course = Fabric.create_course(request.data)
            self.course_list.append(course)
            return HttpResponseRedirect('', request)


class CategoryView(View):
    category_list = []

    def get(self, request):
        categories = self.category_list
        context['categories'] = categories
        return HttpResponse(self.render('category.html', context=context), request)

    def post(self, request):
        if request.data_len:
            category = CategoryFactory.crate(request.data)
            self.category_list.append(category)
            return HttpResponseRedirect('', request)