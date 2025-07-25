from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'  # Создай этот шаблон, если ещё нет
    success_url = reverse_lazy('login')    # После регистрации переходит на страницу входа

    def form_valid(self, form):
        # Сохраняем пользователя, вызов родительского метода вернёт response
        response = super().form_valid(form)
        # Создаём связанный профиль для нового пользователя
        Profile.objects.create(user=self.object)
        return response