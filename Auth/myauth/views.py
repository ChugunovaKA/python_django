from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.views import View


class MyLogoutView(LogoutView):
    next_page = '/'  # страница для переадресации после выхода


class SetCookieView(View):
    def get(self, request):
        response = HttpResponse('Cookie установлена')
        response.set_cookie('mycookie', 'value123', max_age=3600)  # куки на 1 час
        return response


class GetCookieView(View):
    def get(self, request):
        value = request.COOKIES.get('mycookie', 'Значение по умолчанию')
        return HttpResponse(f'Значение cookie: {value}')


class SetSessionView(View):
    def get(self, request):
        request.session['mykey'] = 'value_in_session'
        return HttpResponse('Данные записаны в сессию')


class GetSessionView(View):
    def get(self, request):
        value = request.session.get('mykey', 'Значение по умолчанию')
        return HttpResponse(f'Значение в сессии: {value}')
