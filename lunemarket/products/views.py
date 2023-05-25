from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import QuerySet
from .models.models import Cards, Categories
from django.conf import settings
from products.filters import *


class ProductsView(ListView):
    paginate_by = settings.CATEGORY_PRODUCTS_BATCH_SIZE
    model = Cards
    template_name = "products\\products-listing.html"
    context_object_name = "items"
    _used_model = Categories

    def get_queryset(self):
        category = dashes_to_spaces(self.kwargs.get("category"))
        query_set: QuerySet = Categories.objects.filter(parent=category)

        if not len(query_set):
            query_set: QuerySet = self.model.objects.filter(category=category)
            self._used_model = self.model

        return query_set.order_by("price" if self._used_model == self.model else "title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({"items_is": "categories" if self._used_model == Categories else "cards"})
        return context


class CardView(DetailView):
    model = Cards
    template_name = "products\\product-details.html"
    context_object_name = "item_info"
    slug_field = "title"
    slug_url_kwarg = "title"

    def get_queryset(self):
        prod_title = self.kwargs.get("title")
        query_set: QuerySet = self.model.objects.filter(title=prod_title)

        return query_set.order_by("title")

