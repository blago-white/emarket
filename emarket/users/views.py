from django.db import IntegrityError
from allauth.account.utils import send_email_confirmation
from allauth.account.views import (LoginView,
                                   LogoutView,
                                   SignupView,
                                   PasswordChangeView,
                                   EmailVerificationSentView,
                                   PasswordResetView,
                                   PasswordResetDoneView,
                                   PasswordResetFromKeyView)
from allauth.socialaccount.views import LoginErrorView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpRequest
from django.middleware.csrf import get_token
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, RedirectView, TemplateView
from django.db.models import F, Exists
from products.models.models import Phone
from .mixins import UserLoginRequiredMixin
from .models.models import UserProfile, Notifications
from .forms import RegisterUserForm, ChangeUsernameForm, ChangeEmailForm, ChangeAvatarForm
from .filters import *


__all__ = ["RegisterUserView",
           "UserLoginErrorView",
           "LoginUserView",
           "UserPasswordChangeView",
           "BaseAccountView",
           "AccountInfoView",
           "AccountProductsView",
           "AccountNotificationsView",
           "AccountNotificationDeleteView",
           "LogoutUserView",
           "ChangeAccountDataView",
           "UserEmailVerificationView",
           "ResetUserPasswordView",
           "ResetUserPasswordDoneView",
           "ResetUserPasswordFromKeyView",
           "RedirectToAccountInfoView",
           "AboutInfoView"]


class BaseAccountView:
    _account_sections = ("info", "products", "basket", "notifications")

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


class AboutInfoView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        current_context = super(AboutInfoView, self).get_context_data(**kwargs)

        current_context.update({"custom_bg_img_path": "img/emarket-icon.png"})

        return current_context


class RegisterUserView(SignupView):
    form_class = RegisterUserForm
    template_name = "users/register.html"

    def form_valid(self, form):
        form.instance.username = _get_username_by_mail(mail_adress=form.instance.email)
        http_response = super().form_valid(form=form)

        try:
            self._try_create_empty_user_profile()
        except:
            return super().form_invalid(form=form)

        return http_response

    def _try_create_empty_user_profile(self) -> None:
        new_profile = UserProfile(user=self.user)
        new_profile.full_clean()
        new_profile.save()


class UserLoginErrorView(LoginErrorView):
    template_name = "users/login-error.html"


class LoginUserView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        try:
            del current_context["form"].fields["login"].widget.attrs["placeholder"]
            del current_context["form"].fields["password"].widget.attrs["placeholder"]
        except:
            pass

        return current_context


class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/change-password.html"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        try:
            del current_context["form"].fields["oldpassword"].widget.attrs["placeholder"]
            del current_context["form"].fields["password1"].widget.attrs["placeholder"]
            del current_context["form"].fields["password2"].widget.attrs["placeholder"]

        except:
            pass

        return current_context


class AccountInfoView(BaseAccountView, DetailView):
    model = UserProfile
    template_name = "users/account-info.html"
    context_object_name = "user"
    slug_url_kwarg = "pk"
    slug_field = "pk"

    section = "info"

    def get_object(self, queryset=None):
        try:
            return super(AccountInfoView, self).get_object(queryset=queryset)
        except:
            if self.request.user.id == self.kwargs.get("pk"):
                return self.request.user

            return User.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"change_username_form": ChangeUsernameForm})
        current_context.update({"change_email_form": ChangeEmailForm})
        current_context.update({"change_avatar_form": ChangeAvatarForm})

        try:
            current_context.update({"error": self.request.GET.get("error")})
            current_context.update({"error_field": current_context["error"].split("-")[-1]})
            current_context.update({"error_name": "-".join(current_context["error"].split("-")[0:-1])})
        except:
            pass

        return current_context


class AccountProductsView(BaseAccountView, ListView):
    model = Phone
    template_name = "users/account-cards.html"
    context_object_name = "items"
    section = "products"

    def get_queryset(self):
        user_from_request = super().get_user()[0]

        if self.request.user != user_from_request:
            return self.model.objects.filter(author=user_from_request, products_count__gt=0).order_by("-views")

        return self.model.objects.filter(author=user_from_request).order_by("-views")


class AccountNotificationsView(UserLoginRequiredMixin, BaseAccountView, ListView):
    model = Notifications
    section = "notifications"
    template_name = "users/notifications.html"
    context_object_name = "notifications"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)
        current_context.update({"is_self_account": True})
        current_context.update({"available_themes": (i[0] for i in Notifications.NOTIFICATIONS_THEMES)})

        return current_context

    def get_queryset(self):
        user = self.request.user.id
        return self.model.objects.filter(recipient=user)


class AccountNotificationDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Notifications
    success_url = reverse_lazy("account-notifications")
    section = "notifications"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get("pk"))


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("home")
    template_name = "users/logout.html"


class ChangeAccountDataView(UpdateView):
    model = User

    _avaible_fields_for_update_user = ("username", "email")
    _avaible_fields_for_update_profile = ("avatar", )
    _avaible_fields_for_update = _avaible_fields_for_update_user + _avaible_fields_for_update_profile

    _uncorrect_username_warn = User.username_validator.message
    _exist_username_warn = "A user with that username already exists."

    _field_name: str
    _value_from_request: object

    def get_success_url(self):
        return reverse_lazy("account-info", kwargs={"pk": self.request.user.id})

    def post(self, request, *args, **kwargs):
        self._set_updating_field_name_value_from_request()

        if (not self._field_name) or (self._field_name not in self._avaible_fields_for_update):
            return HttpResponseRedirect(self.get_success_url())

        self._set_user_to_update_by_request()

        if self._value_from_request and self._user_to_update.__dict__.get(self._field_name) != self._value_from_request:
            if self._field_name == "email":
                return HttpResponseRedirect(self._get_redirect_url_for_update_email(email=self._value_from_request))

            try:
                self._try_update_user_field()
            except Exception as exception:
                return HttpResponseRedirect(self._get_redirect_url_by_exception(exception=exception))

        return HttpResponseRedirect(self.get_success_url())

    def _set_updating_field_name_value_from_request(self) -> None:
        self._field_name = self._get_updating_field_name()
        self._value_from_request = self.request.POST.get(self._field_name) or self.request.FILES.get(self._field_name)

    def _get_redirect_url_by_exception(self, exception: Exception) -> str:
        if type(exception) == ValidationError:
            if self._field_name == "username":
                return self._get_url_with_username_error_info(validation_error=exception)
            else:
                return self.get_success_url()
        else:
            return self.get_success_url()

    def _set_user_to_update_by_request(self) -> None:
        self._user_to_update: User = self.model.objects.get(pk=self.request.user.id)

        if self._field_name == "avatar":
            self._user_to_update: UserProfile = UserProfile.objects.get(pk=self.request.user.id)

    def _get_redirect_url_for_update_email(self, email: str) -> str:
        try:
            send_email_confirmation(request=self.request, user=self.request.user, email=email)
        except IntegrityError:
            return _get_url_with_args(url=self.get_success_url(), error="exist-email")
        except:
            return _get_url_with_args(url=self.get_success_url(), error="unexpected-error-email")
        else:
            return reverse_lazy("account_email_verification_sent")

    def _get_updating_field_name(self) -> str:
        if not self.request.POST:
            return

        for avaible_field_name in self._avaible_fields_for_update:
            if self.request.POST.get(avaible_field_name) or self.request.FILES.get(avaible_field_name):
                return avaible_field_name

    def _get_url_with_username_error_info(self, validation_error: ValidationError) -> str:
        if validation_error.error_dict[self._field_name][0].message == self._uncorrect_username_warn:
            error_code = "uncorrect-username"
        elif validation_error.error_dict[self._field_name][0].message == self._exist_username_warn:
            error_code = "exist-username"
        else:
            error_code = "unexpected-error-username"

        return _get_url_with_args(url=self.get_success_url(), error=error_code)

    def _try_update_user_field(self) -> None:
        self._user_to_update.__dict__[self._field_name] = self._value_from_request
        self._user_to_update.full_clean()
        self._user_to_update.save()


class UserEmailVerificationView(EmailVerificationSentView):
    template_name = "users/email-verification-info.html"


class ResetUserPasswordView(PasswordResetView):
    template_name = "users/password-reset-from-anonymous-user.html"

    def get(self, request, *args, **kwargs):
        try:
            return send_reset_password_email(user=request.user)
        except:
            return super(ResetUserPasswordView, self).get(*args, request=request, *kwargs)


class ResetUserPasswordDoneView(PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class ResetUserPasswordFromKeyView(PasswordResetFromKeyView):
    template_name = "users/change-password.html"

    def get_context_data(self, **kwargs):
        print("reset key")
        current_context = super(ResetUserPasswordFromKeyView, self).get_context_data(**kwargs)
        try:
            del current_context["form"].fields["password1"].widget.attrs["placeholder"]
            del current_context["form"].fields["password2"].widget.attrs["placeholder"]
        except:
            pass
        return current_context


class RedirectToAccountInfoView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("account-info", kwargs={"pk": self.request.user.id})


def _get_username_by_mail(mail_adress: str) -> str:
    return "".join(letter for letter in mail_adress.split("@")[0] if letter.isalpha())


def _get_url_with_args(url: str, **url_args) -> str:
    return url + "?" + "&".join([f"{key}={value}" for key, value in zip(url_args.keys(), url_args.values())])


def send_reset_password_email(user: User):
    request = HttpRequest()
    request.method = 'POST'
    request.user = user
    request.META['HTTP_HOST'] = django.conf.settings.HOST_NAME_WITHOUT_PORT

    request.POST = {
        'email': user.email,
        'csrfmiddlewaretoken': get_token(HttpRequest())
    }
    return PasswordResetView.as_view()(request)
