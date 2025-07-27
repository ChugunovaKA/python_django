from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    about_me,
    RegisterView,
    FooBarView,
    users_list,
    profile_detail,  # добавлено
    profile_edit,    # добавлено для редактирования профиля
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", about_me, name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),

    path("users/", users_list, name="users-list"),

    path("profile/<str:username>/", profile_detail, name="profile-detail"),  # просмотр профиля
    path("profile/<str:username>/edit/", profile_edit, name="profile-edit"), # редактирование профиля
]