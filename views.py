from Framework.http_lib import HttpResponse, HttpResponseRedirect
from Framework.view import View
from forms import CourseForm, CategoryForm
from model import Course, Category

context = {
        'index': '/',
        'about': '/about',
        'contacts': '/contacts',
        'course': '/course',
        'category': '/category',
    }


class IndexView(View):
    def get(self, request):
        return HttpResponse(self.render('index.html', context=context), request)


class AboutView(View):

    def get(self, request):
        return HttpResponse(self.render('about.html', context=context), request)


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
    def get(self, request):
        courses = Course.select()
        categories = Category.select()
        context['courses'] = courses
        context['categories'] = categories
        for item in courses:
            print(item.name)
        return HttpResponse(self.render('course.html', context=context), request)

    def post(self, request):
        if request.data_len:
            course = CourseForm(request.data)
            course.create()
            return HttpResponseRedirect('', request)


class CategoryView(View):
    def get(self, request):
        categories = Category.select()
        context['categories'] = categories
        for item in categories:
            print(item.name)
        return HttpResponse(self.render('category.html', context=context), request)

    def post(self, request):
        if request.data_len:
            category = CategoryForm(request.data)
            category.create()
            return HttpResponseRedirect('', request)