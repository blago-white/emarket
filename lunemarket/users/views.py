from django.shortcuts import render
from django.views.generic import CreateView
from django.forms import Form
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
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
    success_url = reverse_lazy("account")

    def get_success_url(self):
        return reverse_lazy("home")
