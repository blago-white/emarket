from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.forms import Form
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm
from products.models.models import Cards
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
    template_name = "users/account-info.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        current_context = super(AccountView, self).get_context_data(**kwargs)
        current_context.update({"current_section": "info"})

        return current_context


class UserAccountCardsView(ListView):
    model = Cards
    template_name = "users/account-cards.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        current_context = super(UserAccountCardsView, self).get_context_data(**kwargs)
        current_context.update({"current_section": "cards"})
        current_context.update({"items_is": "cards"})

        return current_context

    def get_queryset(self):
        return self.model.objects.filter(author=User.objects.filter(id=self.request.user.id)[0])


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("home")
