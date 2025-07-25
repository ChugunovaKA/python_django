from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'  # Шаблон должен быть создан
    success_url = reverse_lazy('login')    # Редирект после регистрации

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response