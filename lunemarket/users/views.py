from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.forms import Form
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.db.models import Count
from .forms import RegisterUserForm
from products.models.models import Cards, Categories
from users.mixins import UserLoginRequiredMixin
from users.models import Notifications
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


class BaseAccountView(UserLoginRequiredMixin):
    _account_sections = ("info", "cards", "categories", "basket", "notifications")

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)
        current_context.update({"current_section": self._get_curren_section()})
        current_context.update({"current_user_account_pk": self.request.user.id})

        if "pk" in self.kwargs:
            current_context.update({"is_self_account": int(self.kwargs.get("pk")) == int(self.request.user.id)})
            current_context.update({"current_user_account_pk": int(self.kwargs.get("pk"))})

        return current_context

    def get_user(self, url_pk_name: str = "pk"):
        if not self.kwargs.get(url_pk_name):
            raise KeyError(f"Not found url-arg: '{url_pk_name=}'")

        return User.objects.filter(id=self.kwargs.get(url_pk_name))

    def _get_curren_section(self):
        try:
            if self.section in self._account_sections:
                return self.section

        except AttributeError:
            raise AttributeError("Field section required if you inherited by 'BaseAccountView'")

        raise ValueError("Not correct section name")


class AccountInfoView(BaseAccountView, DetailView):
    model = User
    template_name = "users/account-info.html"
    context_object_name = "user"
    section = "info"

    def get_queryset(self):
        return super().get_user()


class AccountCardsView(BaseAccountView, ListView):
    model = Cards
    template_name = "users/account-cards.html"
    context_object_name = "items"
    section = "cards"

    def get_queryset(self):
        user = super().get_user()[0]
        return self.model.objects.filter(author=user).order_by("-views")


class AccountCategoriesView(AccountCardsView):
    model = Categories
    section = "categories"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)
        return current_context

    def get_queryset(self):
        user = super().get_user()[0]
        return self.model.objects.filter(author=user)


class AccountNotificationsView(BaseAccountView, ListView):
    model = Notifications
    section = "notifications"
    template_name = "users/notifications.html"
    context_object_name = "notifications"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)
        current_context.update({"is_self_account": True})

        return current_context

    def get_queryset(self):
        user = self.request.user.id
        return self.model.objects.filter(user=user)


class AccountNotificationDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Notifications
    success_url = reverse_lazy("account-notifications")
    section = "notifications"

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs.get("pk"))


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("home")
