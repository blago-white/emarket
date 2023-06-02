from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from products.models.models import Cards
from users.views import BaseAccountView
from .models import ShoppingBasket
from .emails import EmailPurchase
from .filters import *


class ShoppingBasketView(BaseAccountView, ListView):
    model = ShoppingBasket
    template_name = "purchasing\\basket.html"
    context_object_name = "products"
    _section = "basket"

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)


class DeleteProductFromBucketView(BaseAccountView, DeleteView):
    model = ShoppingBasket

    def get_success_url(self):
        return reverse("basket", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        product_data = Cards.objects.filter(title=self.kwargs.get("productid"))[0]
        user = super().get_user()[0]

        return self.model.objects.filter(user=user, product=product_data)[0]


class AddProductToBasket(BaseAccountView, CreateView):
    model = ShoppingBasket
    fields = []

    def get_success_url(self):
        return reverse("basket", kwargs={"pk": self.kwargs.get("pk")})

    def post(self, request, *args, **kwargs):
        return super(AddProductToBasket, self).post(*args, request=request, **kwargs)

    def form_valid(self, form):
        form.instance.user = User.objects.filter(id=self.kwargs.get("pk"))[0]
        form.instance.product = _get_product_by_id(self.kwargs.get("productid"))

        try:
            return super().form_valid(form=form)
        except:
            return HttpResponseRedirect(self.get_success_url())


class BuyProductView(BaseAccountView, DeleteView):
    model = ShoppingBasket

    def get_object(self, queryset=None):
        user_data = self.request.user
        product_data = _get_product_by_id(product_id=self.kwargs.get("productid"))
        return get_object_or_404(ShoppingBasket, user=user_data, product=product_data)

    def delete(self, request, *args, **kwargs):
        send_purchase_info_email(username=user_data.usernamem,
                                 product_title=product_data.title,
                                 product_price=product_data.price)

        return super().delete(*args, request=request, **kwargs)

    def get_success_url(self):
        return reverse("basket", kwargs={"pk": self.kwargs.get("pk")})


def send_purchase_info_email(username: str, product_title: str, product_price: float):
    email_purchase = EmailPurchase(username=username, user_mail="webmaster@localhost")
    email_purchase.send(product_title=product_title, price=price)


def _get_product_by_id(product_id: str) -> Cards:
    return Cards.objects.filter(title=product_id)[0]
