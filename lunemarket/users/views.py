from django.shortcuts import render
from django.views.generic import CreateView
from django.forms import Form
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import RegisterUserForm
from .filters import *


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("account")


class AccountView:
    pass
