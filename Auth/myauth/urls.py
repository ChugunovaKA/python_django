from django.urls import path
from django.contrib.auth.views import LoginView
from .views import MyLogoutView, SetCookieView, GetCookieView

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', MyLogoutView.as_view(), name='logout'),

    path('set-cookie/', SetCookieView.as_view(), name='set_cookie'),
    path('get-cookie/', GetCookieView.as_view(), name='get_cookie'),
]