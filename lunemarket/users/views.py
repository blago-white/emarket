from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.forms import Form
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterUserForm
from .filters import *


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class AccountView(DetailView):
    model = User
    template_name = "users/account.html"
    context_object_name = "user"


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("home")
