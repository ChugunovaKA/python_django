from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .views import (
    MyLogoutView,
    SetCookieView, GetCookieView,
    SetSessionView, GetSessionView,
)

urlpatterns = [
    path('', lambda request: HttpResponse('Главная страница'), name='home'),  # главная страница

    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', MyLogoutView.as_view(), name='logout'),

    path('set-cookie/', SetCookieView.as_view(), name='set_cookie'),
    path('get-cookie/', GetCookieView.as_view(), name='get_cookie'),

    path('set-session/', SetSessionView.as_view(), name='set_session'),
    path('get-session/', GetSessionView.as_view(), name='get_session'),
]