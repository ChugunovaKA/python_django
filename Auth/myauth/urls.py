from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',      # имя шаблона
        redirect_authenticated_user=True        # если пользователь уже аутентифицирован — редирект
    ), name='login'),
    # логаут добавим позже, вместе с остальными views
]