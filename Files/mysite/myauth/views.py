from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile
from .forms import ProfileAvatarForm
from django.contrib.auth.models import User  # импорт для списков пользователей


@login_required
def about_me(request):
    profile = request.user.profile  # Получаем профиль текущего пользователя

    if request.method == 'POST':
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, 'myauth/about-me.html', {
        'form': form,
        'profile': profile,
    })


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'myauth/users_list.html', {'users': users})


@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    can_edit = request.user == user or request.user.is_staff  # можно ли редактировать профиль

    return render(request, "myauth/profile_detail.html", {
        "profile_user": user,
        "profile": profile,
        "can_edit": can_edit,
    })


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_staff:
        return HttpResponseForbidden("Нет доступа на редактирование этого профиля")

    profile = user.profile
    if request.method == "POST":
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("myauth:profile-detail", username=user.username)
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, "myauth/profile_edit.html", {"form": form, "profile_user": user})