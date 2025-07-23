from django.urls import path
from django.contrib.auth.views import LoginView
from .views import MyLogoutView

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]