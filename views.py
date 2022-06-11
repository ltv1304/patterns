from Framework.apps import SMSNotifier, EmailNotifier
from Framework.http_lib import HttpResponse, HttpResponseRedirect, Request
from Framework.middleware import debug
from Framework.view import View
from model import category_serializer, course_serializer, student_serializer

context = {
        'index': '/',
        'about': '/about',
        'contacts': '/contacts',
        'course': '/course',
        'category': '/category',
        'students': '/students'
    }


@debug('test')
class IndexView(View):
    def get(self, request: Request):
        return HttpResponse(self.render('index.html', context=context), request)


class AboutView(View):

    def get(self, request: Request):
        return HttpResponse(self.render('about.html', context=context), request)


class ContactsView(View):

    def get(self, request: Request):
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

    def get(self, request: Request):
        return HttpResponse(self.render('success_page.html'), request)


class CourseView(View):
    course_list = []

    def get(self, request: Request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            context['course_detail'] = course_serializer.find_by_id(pk)
            context['categories'] = category_serializer.get_all()
            return HttpResponse(self.render('course_detail.html', context=context), request)
        else:
            context['courses'] = course_serializer.get_all()
            context['categories'] = category_serializer.get_all()
            return HttpResponse(self.render('course.html', context=context), request)

    def post(self, request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            course_serializer.update(request.data, pk)
            return HttpResponseRedirect('', request)
        else:
            course_serializer.insert(request.data)
            return HttpResponseRedirect('', request)


class CategoryView(View):

    def get(self, request: Request):
        categories = category_serializer.get_all()
        context['categories'] = categories
        return HttpResponse(self.render('category.html', context=context), request)

    def post(self, request: Request):
        if request.data_len:
            category_serializer.insert(request.data)
            return HttpResponseRedirect('', request)


@debug('test1')
class StudentsView(View):

    def get(self, request: Request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            context['student'] = student_serializer.find_by_id(pk)
            context['courses'] = course_serializer.get_all()
            return HttpResponse(self.render('student_detail.html', context=context), request)
        else:
            context['students_list'] = student_serializer.get_all()
            return HttpResponse(self.render('students.html', context=context), request)

    def post(self, request: Request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            student_serializer.update(request.data, pk)
            return HttpResponseRedirect('', request)
        else:
            student_serializer.insert(request.data)
            return HttpResponseRedirect('', request)
