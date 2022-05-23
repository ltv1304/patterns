from Framework.http_lib import HttpResponse, HttpResponseRedirect
from Framework.view import View

context = {
        'index': '/',
        'about': '/about',
        'contacts': '/contacts',
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
