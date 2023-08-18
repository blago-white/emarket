from django.http.response import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db.models import Count, Max, Avg, F, Sum, QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView
from django.conf import settings

from products.forms import AddProductForm, EditProductForm
from users.mixins import UserLoginRequiredMixin
from .models.models import Category, Phone
from .models.utils import increment_product_views, convert_category_filters_to_product_filters
from .filters import *


class HomePageProductsView(ListView):
    model = Category
    template_name = 'home/home.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(parent=None)


class ProductsView(ListView):
    paginate_by = settings.CATEGORY_PRODUCTS_BATCH_SIZE
    model = Phone
    template_name = "products/products-listing.html"
    context_object_name = "items"
    _max_product_price: int
    _product_id: int = None

    def get_queryset(self):
        category = self.kwargs.get("category")
        prices_range = self._get_acceptable_price_range_bounds()

        filters = {"price__gte": prices_range[0], "price__lte": prices_range[1]}

        if self.request.GET.get("stortage") or self.request.GET.get("color"):
            self._add_multiple_url_filtring_args(filters=filters)

        return self._get_queryset(
            category=category,
            **filters
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        current_context = super().get_context_data(object_list=None, **kwargs)
        self._complement_context(current_context)
        return current_context

    def get_ordering(self):
        return get_ordering_field_from_url_arg(url_arg=self.request.GET.get("price"), field="price")

    def render_to_response(self, context, **response_kwargs):
        if self._product_id:
            return redirect(reverse("product-card", kwargs={"pk": self._product_id}))
        return super(ProductsView, self).render_to_response(context=context, **response_kwargs)

    def _add_multiple_url_filtring_args(self, filters: dict) -> None:
        multiple_url_filtering_args = {"stortage": self.request.GET.get("stortage"),
                                       "color": self.request.GET.get("color")}

        for multiple_url_filtering_arg in multiple_url_filtering_args:
            if not multiple_url_filtering_args[multiple_url_filtering_arg]:
                continue

            filters.update({f"phone__{multiple_url_filtering_arg}__in": list()})
            from_db_choices_dict = Phone.STORTAGE_ID_BY_SIZE if multiple_url_filtering_arg == "stortage" else Phone.COLOR_CODE_BY_NAME

            for url_filtering_arg in self.request.GET.getlist(multiple_url_filtering_arg):
                try:
                    filters[
                        f"phone__{multiple_url_filtering_arg}__in"
                    ].append(
                        from_db_choices_dict[
                            int(url_filtering_arg) if url_filtering_arg.isdigit() else url_filtering_arg
                        ]
                    )
                except:
                    pass

    def _get_queryset(self, category: str, **query_filters) -> QuerySet:
        queryset = self._get_categories_queryset(parent_category=category, **query_filters)

        if not queryset.count():
            convert_category_filters_to_product_filters(query_filters=query_filters)
            queryset = self._get_products_queryset(category=category, **query_filters)

            if queryset.count() == 1:
                self._product_id = queryset[0].id

        return queryset

    def _get_categories_queryset(self, parent_category, **query_filters) -> QuerySet:
        return Category.objects.filter(
            parent=parent_category,
        ).values("title").annotate(
            price=Avg(F("phone__price")),
            photo=Max(F("phone__photo")),
            _count_items_in=Sum("phone__products_count")
        ).filter(
            **query_filters, _count_items_in__gt=0
        ).annotate(
            count_products_in=Count("phone")
        ).order_by(
            self.get_ordering()
        )

    def _get_products_queryset(self, category, **query_filters):
        return Phone.objects.filter(
            category=category,
            products_count__gt=0,
            **query_filters
        ).order_by(
            self.get_ordering()
        )

    def _complement_context(self, current_context: dict) -> None:
        self._set_max_product_price()
        price_range_bounds = self._get_acceptable_price_range_bounds(max_price_bound=self._max_product_price)
        filters_window_display = int(self.request.GET.get("filters", 0))

        current_context.update({
            "filters": filters_window_display,
            "url_args": compile_url_args_for_pagination(
                price=get_url_arg_from_ordering_field(field=self.get_ordering()),
                min_=price_range_bounds[0],
                filters=filters_window_display,
                max_=price_range_bounds[1],
                stortage=self.request.GET.getlist("stortage"),
                color=self.request.GET.getlist("color"),
            ),
            "url_args_invert_sorting": compile_url_args_for_pagination(
                price=invert_sorting(get_url_arg_from_ordering_field(field=self.get_ordering())),
                min_=price_range_bounds[0],
                filters=filters_window_display,
                max_=price_range_bounds[1],
                stortage=self.request.GET.getlist("stortage"),
                color=self.request.GET.getlist("color"),
            ),
            "max_item_price": self._max_product_price,
            "price_lower_bound": price_range_bounds[0],
            "price_upper_bound": price_range_bounds[-1],
            "supported_stortage_sizes": Phone.STORTAGE_ID_BY_SIZE.keys(),
            "supported_colors": tuple(Phone.COLOR_CODE_BY_NAME.keys()),
            "supported_color_codes": tuple(Phone.COLOR_CODE_BY_NAME.values()),
            "category_name": self.kwargs.get("category")
        })

        if self.request.GET.getlist("stortage") or self.request.GET.getlist("color"):
            for url_multiple_arg_name in "stortage", "color":
                current_context.update(
                    {f"selected_{url_multiple_arg_name}_values":
                        tuple(
                            int(url_value) if url_value.isdigit() else url_value for url_value in
                            self.request.GET.getlist(url_multiple_arg_name)
                        )}
                )

    def _get_acceptable_price_range_bounds(self, max_price_bound=5000) -> tuple:
        try:
            bounds = int(self.request.GET.get("min", 0)), int(self.request.GET.get("max", max_price_bound))
        except:
            return 0, max_price_bound

        if bounds[0] > bounds[1]:
            return 0, bounds[1]

        return int(self.request.GET.get("min", 0)), int(self.request.GET.get("max", max_price_bound))

    def _set_max_product_price(self) -> int:
        max_price = Phone.objects.all().aggregate(Max('price'))["price__max"]

        if max_price:
            self._max_product_price = max_price + 1
        else:
            self._max_product_price = 5000


class ProductDetailView(DetailView):
    model = Phone
    template_name = "products/product-details.html"
    context_object_name = "item_info"

    _product_author_id: int
    _product_views: int

    def get_object(self, queryset=None):
        card_specs: Phone = Phone.objects.get(pk=self.kwargs.get("pk"))
        self._product_author_id = card_specs.author.id
        self._product_views = card_specs.views

        if not self.request.__dict__.get("user") or self.request.user != card_specs.author:
            increment_product_views(phone=card_specs)

        return card_specs

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({
            "viewer_is_author": self.request.__dict__.get("user") and self.request.user.id == self._product_author_id
        })
        current_context.update({"stortage": current_context["item_info"].get_stortage_display()})
        current_context.update({"views": self._product_views})

        return current_context

    def render_to_response(self, context, **response_kwargs):
        if not context["viewer_is_author"] and self.object.products_count < 1:
            return HttpResponseRedirect(redirect_to=reverse("product-not-exist"))

        return super().render_to_response(context=context, **response_kwargs)


class AddProductView(UserLoginRequiredMixin, CreateView):
    model = Phone
    template_name = "products/add-product.html"
    form_class = AddProductForm
    _created_product_category_name: str

    def get_success_url(self):
        return reverse("category-products", kwargs={"category": self._created_product_category_name})

    def form_valid(self, form):
        form.instance.author, self._created_product_category_name = self.request.user, form.instance.category

        try:
            target_category = Category.objects.get(title=spaces_to_dashes(form.instance.title))
        except:
            new_category = Category(title=form.instance.title,
                                    parent=form.instance.category,
                                    photo=form.instance.photo)
            try:
                new_category.full_clean()
            except ValidationError:
                return super().form_invalid(form=form)
            else:
                new_category.save()

            target_category = new_category

        form.instance.category = target_category

        return super(AddProductView, self).form_valid(form=form)


class EditProductView(AddProductView):
    form_class = EditProductForm
    _current_product: Phone

    def get(self, request, *args, **kwargs):
        self.get_current_product()
        return super(EditProductView, self).get(*args, request=request, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['instance'] = self._current_product
        kwargs['instance'].title = dashes_to_spaces(string=kwargs['instance'].readable_title())

        return kwargs

    def get_current_product(self) -> Phone:
        self._current_product = self.model.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"current_product": self._current_product})

        return current_context


class DeleteUserProductView(UserLoginRequiredMixin, DeleteView):
    model = Phone

    def get_success_url(self):
        return reverse("account-products", kwargs={"pk": self.request.user.id})

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get("pk"), author=self.request.user)


class ProductDoesNotExistWarningView(UserLoginRequiredMixin, TemplateView):
    template_name = "products/product-does-not-exist.html"

