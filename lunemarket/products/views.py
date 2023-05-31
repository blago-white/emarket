from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import QuerySet
from .models.models import Cards, Categories
from django.conf import settings
from django.urls import reverse_lazy
from products.forms import AddProductForm, AddCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
            min_range = self._get_acceptable_range_price()
            query_set: QuerySet = self.model.objects.filter(category=category, price__gte=min_range)
            self._used_model = self.model

        return query_set.order_by((self.get_ordering() if self._used_model == self.model else "title"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        context.update({"items_is": "categories" if self._used_model == Categories else "cards"})
        context.update({"filters": "filters" in self.request.GET.keys()})
        context.update({"url_args": compile_url_args_for_pagination(
            price=get_url_arg_from_ordering_field(field=self.get_ordering()),
            min_=self._get_acceptable_range_price(),
            filters="filters" in self.request.GET.keys(),
        )})
        context.update({"url_args_invert_sorting": compile_url_args_for_pagination(
            price=invert_sorting(get_url_arg_from_ordering_field(field=self.get_ordering())),
            min_=self._get_acceptable_range_price(),
            filters="filters" in self.request.GET.keys(),
        )})
        context.update({"max_item_price": Cards.objects.aggregate(Max('price'))["price__max"]})
        context.update({"min_price": self._get_acceptable_range_price()})

        return context

    def get_ordering(self):
        return get_ordering_field_from_url_arg(url_arg=self.request.GET.get("price"), field="price")

    def _get_acceptable_range_price(self):
        try:
            return int(self.request.GET.get("min", 0))
        except:
            return 0


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


class AddProductView(LoginRequiredMixin, CreateView):
    model = Cards
    template_name = "products\\add-product.html"
    form_class = AddProductForm

    def get_success_url(self):
        return reverse_lazy("home")


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Categories
    template_name = "products\\add-category.html"
    form_class = AddCategoryForm

    def get_success_url(self):
        return reverse_lazy("home")

