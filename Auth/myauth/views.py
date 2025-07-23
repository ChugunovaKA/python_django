from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

class MyLogoutView(LogoutView):
    next_page = '/'
