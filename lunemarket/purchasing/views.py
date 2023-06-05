from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from products.models.models import Cards
from users.views import BaseAccountView
from users.mixins import UserLoginRequiredMixin
from users.models import Notifications
from . import DEFAULT_PURCHASE_MESSAGE_FOR_OWNER
from .models import ShoppingBasket
from .emails import EmailPurchase
from .filters import *


class ShoppingBasketView(BaseAccountView, ListView):
    model = ShoppingBasket
    template_name = "purchasing\\basket.html"
    context_object_name = "products"
    section = "basket"

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)
        current_context.update({"is_self_account": True})

        return current_context

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)


class DeleteProductFromBucketView(UserLoginRequiredMixin, DeleteView):
    model = ShoppingBasket

    def get_success_url(self):
        return reverse("basket")

    def get_object(self, queryset=None):
        product_data = Cards.objects.filter(title=self.kwargs.get("productid"))[0]
        user = self.request.user

        return self.model.objects.filter(user=user, product=product_data)[0]


class AddProductToBasketView(UserLoginRequiredMixin, CreateView):
    model = ShoppingBasket
    fields = []

    def get_success_url(self):
        return reverse("basket")

    def post(self, request, *args, **kwargs):
        return super().post(*args, request=request, **kwargs)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = _get_product_by_id(self.kwargs.get("productid"))

        if form.instance.product.author.id == self.request.user.id:
            return self.form_invalid(form=form)

        try:
            return super().form_valid(form=form)
        except:
            return HttpResponseRedirect(self.get_success_url())


class BuyProductView(UserLoginRequiredMixin, DeleteView):
    model = ShoppingBasket
    _user_data: User
    _product_data: Cards

    def post(self, request, *args, **kwargs):
        self._user_data = self.request.user
        self._product_data = _get_product_by_id(product_id=self.kwargs.get("productid"))

        return super().post(*args, request=request, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(ShoppingBasket, user=self._user_data, product=self._product_data)

    def form_valid(self, form):
        _send_purchase_info_email(user=self._user_data, product=self._product_data)
        _add_purchase_notification_for_owner(purchaser=self.request.user,
                                             owner=self._product_data.author,
                                             product=self._product_data)
        return super().form_valid(form=form)

    def get_success_url(self):
        return reverse("basket")


def _add_purchase_notification_for_owner(purchaser: User, owner: User, product: Cards) -> None:
    notification_text = _fill_purchase_notification_for_owner(template=DEFAULT_PURCHASE_MESSAGE_FOR_OWNER,
                                                              purchaser=purchaser,
                                                              product=product)
    notification = Notifications(user=owner, text=notification_text, theme="pur")
    notification.save()


def _send_purchase_info_email(user: User, product: Cards) -> None:
    email_purchase = EmailPurchase(username=user.username, user_mail=user.email)
    email_purchase.send(product_title=product.title, price=product.price)


def _get_product_by_id(product_id: str) -> Cards:
    return Cards.objects.filter(title=product_id)[0]


def _fill_purchase_notification_for_owner(template: str, purchaser: User, product: Cards) -> str:
    return template.format(username=purchaser.username, productname=product.title, usermail=purchaser.email, price=product.price)
