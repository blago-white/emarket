import django.http
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import QuerySet
from .models.models import Category, Phone
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import F, Value
from django.db.models.functions import Concat
from products.forms import AddCategoryForm, AddProductForm
from users.mixins import UserLoginRequiredMixin
from .filters import dashes_to_spaces

from products.filters import *

from django.db.models import Count, Max, Min, Exists, Avg


class ProductsView(ListView):
    paginate_by = settings.CATEGORY_PRODUCTS_BATCH_SIZE
    model = Phone
    template_name = "products\\products-listing.html"
    context_object_name = "items"
    _max_product_price: int
    _filters_required: bool = True

    def get_queryset(self):
        category = self.kwargs.get("category")
        prices_range = self._get_acceptable_price_range_bounds()

        return self._get_queryset(
            **{"category": category, "price__gte": prices_range[0], "price__lte": prices_range[1]}
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        current_context = super().get_context_data(object_list=None, **kwargs)
        self._complement_context(current_context)
        return current_context

    def get_ordering(self):
        return get_ordering_field_from_url_arg(url_arg=self.request.GET.get("price"), field="price")

    # def _set_filters_required(self, phones_query_set: QuerySet, categories_query_set: QuerySet) -> bool:
    #     self._filters_required = bool(phones_query_set) or bool([True for category in categories_query_set if len(category.phone_set)])

    def _get_queryset(self, **query_filters) -> QuerySet:
        print(query_filters)
        query_set = (
            Category.objects.filter(
                parent=query_filters.get("category")
            ).extra(select={"is_category": True}).values("is_category").annotate(
                title=F("title"),
                id=Min("baseproduct__id"),
                price=Avg(F("baseproduct__price")),
                photo=Max("photo"),
                color=Value("", output_field=django.db.models.CharField())
            ).filter(baseproduct__price__gte=query_filters.get("price__gte"),
                     baseproduct__price__lte=query_filters.get("price__lte")).union(
                Phone.objects.filter(**query_filters).extra(select={"is_category": False}).values(
                    "is_category", "title", "id", "price", "photo", "color"
                )
            )
        ).order_by(self.get_ordering())

        return query_set

    def _complement_context(self, current_context: dict) -> None:
        self._set_max_product_price()

        price_range_bounds = self._get_acceptable_price_range_bounds(max_price_bound=self._max_product_price)

        current_context.update({
            "filters": int("filters" in self.request.GET.keys()),
            "url_args": compile_url_args_for_pagination(
                price=get_url_arg_from_ordering_field(field=self.get_ordering()),
                min_=price_range_bounds[0],
                filters=int("filters" in self.request.GET.keys()),
                max_=price_range_bounds[1]
            ),
            "url_args_invert_sorting": compile_url_args_for_pagination(
                price=invert_sorting(get_url_arg_from_ordering_field(field=self.get_ordering())),
                min_=price_range_bounds[0],
                filters=int("filters" in self.request.GET.keys()),
                max_=price_range_bounds[1]
            ),
            "max_item_price": self._max_product_price,
            "price_lower_bound": price_range_bounds[0],
            "price_upper_bound": price_range_bounds[-1],
            "filters_required": self._filters_required,
        })

    def _get_acceptable_price_range_bounds(self, max_price_bound=5000) -> tuple:
        try:
            bounds = int(self.request.GET.get("min", 0)), int(self.request.GET.get("max", max_price_bound))
        except:
            return 0, max_price_bound

        if bounds[0] > bounds[1]:
            return 0, bounds[1]

        return int(self.request.GET.get("min", 0)), int(self.request.GET.get("max", max_price_bound))

    def _set_max_product_price(self) -> int:
        self._max_product_price = int(Phone.objects.all().aggregate(Max('price'))["price__max"]) + 1


class ProductDetailView(DetailView):
    model = Phone
    template_name = "products\\product-details.html"
    context_object_name = "item_info"

    _product_author_id: int
    _color: str

    def get_object(self, queryset=None):
        card_specs: Phone = Phone.objects.get(pk=self.kwargs.get("pk"))
        self._product_author_id = card_specs.author.id

        _increment_product_views(card=card_specs)

        return card_specs

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        viewer_is_author = self.request.user.id == self._product_author_id
        current_context.update({"viewer_is_author": viewer_is_author})

        return current_context


class AddProductView(UserLoginRequiredMixin, CreateView):
    model = Phone
    template_name = "products\\add-product.html"
    form_class = AddProductForm
    _created_product_category_name: str

    def get_success_url(self):
        return reverse("category-products", kwargs={"category": self._created_product_category_name})

    def form_valid(self, form):
        form.instance.author = self.request.user
        self._created_product_category_name = form.instance.category

        if Phone.objects.filter(title=spaces_to_dashes(form.instance.title)).exists():
            new_category = Category(title=form.instance.title,
                                    parent=form.instance.category,
                                    photo=form.instance.photo,
                                    )

            try:
                new_category.full_clean()
            except ValidationError:
                return super().form_invalid(form=form)
            else:
                new_category.save()

            current_card = Phone.objects.get(title=spaces_to_dashes(form.instance.title))
            current_card.category = new_category
            current_card.save()

            form.instance.category = new_category

            self._created_product_category_name = new_category

        return super(AddProductView, self).form_valid(form=form)


class EditProductView(AddProductView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['instance'] = self.model.objects.get(pk=self.kwargs.get("pk"))
        kwargs['instance'].title = dashes_to_spaces(string=kwargs['instance'].title)

        return kwargs


class DeleteUserProduct(UserLoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("basket")
    model = Phone

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get("pk"))


def _increment_product_views(card: Phone):
    card.views = F("views") + 1
    card.save()
