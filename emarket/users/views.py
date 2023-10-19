import abc

from allauth.account.utils import send_email_confirmation
from allauth.account import views as allauth_views
from allauth.socialaccount.views import LoginErrorView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators import csrf
from django.views import generic
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse

from emarket import config
from products.models.models import Phone
from .forms import RegisterUserForm, ChangeUsernameForm, ChangeEmailForm, ChangeAvatarForm
from .mixins import UserLoginRequiredMixin
from .models.models import UserProfile, Notifications, DistributionDeliveredMessage
from .services import users, passwords, urls, views, models
from .utils import profile_errors
from .utils.profile_errors import username_errors, email_errors, base

from . import sections

from .filters import *


__all__ = ["RegisterUserView", "UserLoginErrorView", "LoginUserView",
           "UserPasswordChangeView", "BaseAccountView", "AccountInfoView",
           "AccountProductsView", "AccountNotificationsView", "AccountNotificationDeleteView",
           "LogoutUserView", "ChangeAccountDataView", "UserEmailVerificationView",
           "ResetUserPasswordView", "ResetUserPasswordDoneView", "ResetUserPasswordFromKeyView",
           "RedirectToAccountInfoView", "AboutInfoView", "DistributionDeliveredView"]


class BaseAccountView(metaclass=abc.ABCMeta):  # pragma: no cover
    @property
    @abc.abstractmethod
    def section(self) -> str:
        pass

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"current_section": self._get_curren_section().section_name})
        current_context.update({"account_user": self.request.user})

        if account_owner_id := self.kwargs.get("pk"):
            current_context.update({"is_self_account": int(account_owner_id) == int(self.request.user.id)})
            current_context.update({"account_user": User.objects.get(pk=account_owner_id)})

        if current_context["current_section"] == "info":
            current_context.update(
                {"current_account_avatar_url": users.get_user_avatar_url(current_context["account_user"].id)}
            )

        return current_context

    def get_user(self, url_pk_name: str = "pk") -> User:
        if not self.kwargs.get(url_pk_name):
            raise KeyError(f"Not found url-arg: '{url_pk_name=}'")

        return User.objects.filter(id=self.kwargs.get(url_pk_name)).first()

    def _get_curren_section(self) -> sections.BaseAccountSection:
        try:
            if self.section.__bases__[0] == sections.BaseAccountSection:
                return self.section

        except:
            raise AttributeError(
                "Field 'section' required if you inherited by 'BaseAccountView'"
            )

        raise ValueError("Not correct section name")


class AboutInfoView(generic.TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        current_context = super(AboutInfoView, self).get_context_data(**kwargs)

        current_context.update({"custom_bg_img_path": "img/emarket-icon.png"})

        return current_context


class RegisterUserView(allauth_views.SignupView):
    form_class = RegisterUserForm
    template_name = "users/register.html"

    def form_valid(self, form):
        form.instance.username = users.get_username_by_mail(mail_adress=form.instance.email)
        success_response = super().form_valid(form=form)

        try:
            self._create_empty_user_profile()
        except:
            return super().form_invalid(form=form)

        return success_response

    def _create_empty_user_profile(self) -> None:
        UserProfile(user=self.user).save()


class UserLoginErrorView(LoginErrorView):
    template_name = "users/login-error.html"


class LoginUserView(allauth_views.LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        try:
            for field in current_context["form"].fields.values():
                del field.widget.attrs["placeholder"]
        except:
            pass

        return current_context


class UserPasswordChangeView(allauth_views.PasswordChangeView):
    template_name = "users/change-password.html"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        try:
            for field in current_context["form"].fields.values():
                del field.widget.attrs["placeholder"]
        except:
            pass

        return current_context


class AccountInfoView(BaseAccountView, generic.DetailView):
    model = UserProfile
    template_name = "users/account-info.html"
    context_object_name = "user"
    slug_url_kwarg = "pk"
    slug_field = "pk"

    section = sections.InfoAccountSection

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"change_username_form": ChangeUsernameForm})
        current_context.update({"change_email_form": ChangeEmailForm})
        current_context.update({"change_avatar_form": ChangeAvatarForm})

        if (profile_data_error := self._get_error_from_url()) is not None:
            current_context.update({"error": profile_data_error.code})
            current_context.update({"error_field": profile_data_error.field})
            current_context.update({"error_name": profile_data_error.message})

        return current_context

    def _get_error_from_url(self) -> base.BaseUserProfieDataError | None:
        return profile_errors.get_error_by_code(code=self.request.GET.get("error"))


class AccountProductsView(BaseAccountView, generic.ListView):
    model = Phone
    template_name = "users/account-cards.html"
    context_object_name = "items"

    section = sections.ProductsAccountSection

    def get_queryset(self):
        user_from_url = self.get_user()

        if self.request.user != user_from_url:
            return self.model.objects.filter(author=user_from_url, products_count__gt=0).order_by("-views")

        return self.model.objects.filter(author=user_from_url).order_by("-views")


class AccountNotificationsView(UserLoginRequiredMixin,
                               BaseAccountView,
                               generic.ListView):
    model = Notifications
    template_name = "users/notifications.html"
    context_object_name = "notifications"

    section = sections.NotificationsAccountSection

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"is_self_account": True})
        current_context.update({"available_themes": (i[0] for i in Notifications.NOTIFICATIONS_THEMES)})

        return current_context

    def get_queryset(self):
        return self.model.objects.filter(recipient=self.request.user)


class AccountNotificationDeleteView(UserLoginRequiredMixin,
                                    generic.DeleteView):
    model = Notifications
    success_url = reverse_lazy("account-notifications")

    section = sections.NotificationsAccountSection

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get("pk"))


class LogoutUserView(allauth_views.LogoutView):
    next_page = reverse_lazy("home")
    template_name = "users/logout.html"


class ChangeAccountDataView(generic.UpdateView):
    model = User

    _field_name: str
    _value_from_request: object

    def get_success_url(self):
        return reverse_lazy("account-info", kwargs={"pk": self.request.user.id})

    def post(self, request, *args, **kwargs):
        self._set_updating_field_name_value_from_request()

        if ((not self._field_name) or
                (self._field_name not in
                 config.AVAILABLE_FOR_CHANGE_PROFILE_FIELDS)):
            return HttpResponseRedirect(self.get_success_url())

        self._set_user_to_update_by_request()

        if (not self._value_from_request or
                self._user_to_update.__dict__.get(
                    self._field_name
                ) == self._value_from_request):
            return HttpResponseRedirect(self.get_success_url())

        if self._field_name == config.EMAIL_PROFILE_FIELD_NAME:
            return views.confirm_user_email(request=request, email=self._value_from_request)

        try:
            models.try_update_user_profile_field(user=self._user_to_update,
                                                 field=self._field_name,
                                                 new_value=self._value_from_request)
        except Exception as exception:
            return HttpResponseRedirect(self._get_redirect_url_by_exception(exception=exception))

        return HttpResponseRedirect(self.get_success_url())

    def _set_updating_field_name_value_from_request(self) -> None:
        self._field_name = self._get_updating_field_name()
        self._value_from_request = (self.request.POST.get(self._field_name) or
                                    self.request.FILES.get(self._field_name))

    def _get_redirect_url_by_exception(self, exception: Exception) -> str:
        if (type(exception) == ValidationError and
                self._field_name == config.USERNAME_PROFILE_FIELD_NAME):
            return self._get_url_with_username_error_code(validation_error=exception)

        return self.get_success_url()

    def _set_user_to_update_by_request(self) -> None:
        self._user_to_update: User = self.model.objects.get(
            pk=self.request.user.id
        )

        if self._field_name == config.AVATAR_PROFILE_FIELD_NAME:
            self._user_to_update: UserProfile = UserProfile.objects.get(
                pk=self.request.user.id
            )

    def _get_updating_field_name(self) -> str:
        if not self.request.POST:
            return

        for available_field_name in config.AVAILABLE_FOR_CHANGE_PROFILE_FIELDS:
            if (self.request.POST.get(available_field_name) or
                    self.request.FILES.get(available_field_name)):
                return available_field_name

    def _get_url_with_username_error_code(self, validation_error: ValidationError) -> str:
        error_code = views.get_username_error_code(
            validation_error=validation_error,
            field_name=self._field_name
        )

        return urls.get_url_with_args(url=self.get_success_url(), error=error_code)


class UserEmailVerificationView(allauth_views.EmailVerificationSentView):
    template_name = "users/email-verification-info.html"


class ResetUserPasswordView(allauth_views.PasswordResetView):
    template_name = "users/password-reset-from-anonymous-user.html"

    def get(self, request, *args, **kwargs):
        try:
            return allauth_views.PasswordResetView.as_view()(
                passwords.get_reset_password_request(user=request.user)
            )
        except:
            return super(ResetUserPasswordView, self).get(*args, request=request, *kwargs)


class ResetUserPasswordDoneView(allauth_views.PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class ResetUserPasswordFromKeyView(
    allauth_views.PasswordResetFromKeyView
):  # pragma: no  cover
    template_name = "users/change-password.html"

    def get_context_data(self, **kwargs):
        current_context = super(ResetUserPasswordFromKeyView, self).get_context_data(**kwargs)
        try:
            for field in current_context["form"].fields.values():
                del field.widget.attrs["placeholder"]
        except:
            pass
        return current_context


class RedirectToAccountInfoView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("account-info", kwargs={"pk": self.request.user.id})


@method_decorator(csrf.csrf_exempt, name="dispatch")
class DistributionDeliveredView(generic.CreateView):
    http_method_names = ["post",
                         "head",
                         "options",
                         "trace"]

    def post(self, request, *args, **kwargs):
        self._on_delivered_successful(request=request)
        return JsonResponse({"OK": True})

    def _on_delivered_successful(self, request: HttpRequest):
        self._set_delivered_status_for_user(
            user_ipv4=get_user_ip_from_request(request=request)
        )

    @staticmethod
    def _set_delivered_status_for_user(user_ipv4: str):
        DistributionDeliveredMessage(ip=user_ipv4).save()
