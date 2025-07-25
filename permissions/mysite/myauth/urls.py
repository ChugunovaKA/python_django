from django.urls import path
from django.contrib.auth import views as auth_views  # импорт стандартных views

from .views import (
    # AboutMeView,  # временно убрали, чтобы убрать ошибку импорта
    UserRegisterView,  # импортируем регистрацию
)

app_name = "myauth"

urlpatterns = [
    # path("about-me/", AboutMeView.as_view(), name="about-me"),  # временно отключено

    path(
        "login/",
        auth_views.LoginView.as_view(template_name="myauth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),  # при выходе редиректим на логин
        name="logout",
    ),

    path(
        "register/",
        UserRegisterView.as_view(),
        name="register",
    ),
]