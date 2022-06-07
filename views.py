from Framework.apps import SMSNotifier, EmailNotifier
from Framework.http_lib import HttpResponse, HttpResponseRedirect
from Framework.middleware import debug
from Framework.view import View
from model import CategoryFactory, Fabric, StudentFactory

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
    course_list = []

    def get(self, request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            context['course_detail'] = self.get_course(pk)
            context['categories'] = CategoryView.category_list
            return HttpResponse(self.render('course_detail.html', context=context), request)
        else:
            context['courses'] = self.course_list
            context['categories'] = CategoryView.category_list
            return HttpResponse(self.render('course.html', context=context), request)

    def post(self, request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            course = self.get_course(pk)
            Fabric.change_course(course, request.data)
            return HttpResponseRedirect('', request)
        else:
            course = Fabric.create_course(request.data)
            course.attach(SMSNotifier())
            course.attach(EmailNotifier())
            pk = int(course.category)
            category = CategoryView.get_category(pk)
            category.course_list.append(course)
            self.course_list.append(course)
            return HttpResponseRedirect('', request)

    @classmethod
    def get_course(cls, pk):
        for course in cls.course_list:
            if course.id == pk:
                return course


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

    @classmethod
    def get_category(cls, pk):
        for category in cls.category_list:
            if category.id == pk:
                return category


@debug('test1')
class StudentsView(View):
    students_list = []

    def get(self, request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            student = self.get_student(pk)
            context['courses'] = CourseView.course_list
            context['student'] = student

            return HttpResponse(self.render('student_detail.html', context=context), request)
        else:
            students = self.students_list
            context['students_list'] = students
            return HttpResponse(self.render('students.html', context=context), request)

    def post(self, request):
        if request.query.get('pk'):
            pk = int(request.query['pk'][0])
            student = self.get_student(pk)
            courses = self.process_course_data(request.data)
            student.manage_course(courses)
            for course_pk in courses:
                course = CourseView.get_course(course_pk)
                course.student_list.append(student)
            return HttpResponseRedirect('', request)
        else:
            student = StudentFactory.crate(request.data)
            self.students_list.append(student)
            return HttpResponseRedirect('', request)

    @classmethod
    def get_student(cls, pk):
        for student in cls.students_list:
            if student.id == pk:
                return student

    @staticmethod
    def process_course_data(raw_data):
        course_fields = raw_data.split('&')
        course_list = []
        for field in course_fields:
            key, val = field.split('=', 1)
            course_list.append(int(val))
        return course_list