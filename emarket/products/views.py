from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView

from products.forms import AddProductForm, EditProductForm
from users.mixins import UserLoginRequiredMixin
from emarket import config

from .models.models import Category, Phone, BaseProduct
from .models.utils import increment_product_views, convert_category_filters_to_product_filters
from .services import utils as services_utils, urls as urls_services
from .services.models_services import category as category_model_services, phone as phone_model_services

from .filters import *


class HomePageProductsView(ListView):
    model = Category
    template_name = 'home/home.html'
    context_object_name = 'categories'

    def get_queryset(self) -> QuerySet:
        return category_model_services.get_main_categories()


class ProductsView(ListView):
    paginate_by = config.CATEGORY_PRODUCTS_BATCH_SIZE
    model = Phone
    template_name = "products/products-listing.html"
    context_object_name = "items"

    _MULTIPLE_VALUES_URL_ARGS = "storage", "color"

    _CHOISES_VALUES_FOR_CODES_FOR_FIELD = {
        _MULTIPLE_VALUES_URL_ARGS[0]: {storage_size: storage_id for storage_id, storage_size in Phone.STORTAGE_SIZES},
        _MULTIPLE_VALUES_URL_ARGS[1]: {color_name: color_code for color_code, color_name in Phone.BASE_COLORS}
    }

    _CHOISES_LIST_FOR_FIELD = {_MULTIPLE_VALUES_URL_ARGS[0]: Phone.STORTAGE_SIZES,
                               _MULTIPLE_VALUES_URL_ARGS[1]: Phone.BASE_COLORS}

    _max_product_price: int = None
    _product_id: int = None
    _ordering_field: str = None

    def setup(self, request, *args, **kwargs):
        super().setup(*args, request=request, **kwargs)
        self._set_max_product_price()
        self._set_ordering_field(request=request)

    def get_queryset(self):
        prices_range = services_utils.get_product_prices_bounds(
            request_get_args=self.request.GET, max_price_bound=self._max_product_price
        )

        filters = dict(price__gte=prices_range[0], price__lte=prices_range[1])

        self._add_multiple_url_filtring_args(filters=filters)

        return self._get_queryset(category=self.kwargs.get("category"), **filters)

    def get_context_data(self, *, object_list=None, **kwargs):
        current_context = super().get_context_data(**kwargs)
        self._complement_context(current_context)
        return current_context

    def render_to_response(self, context, **response_kwargs):
        if self._product_id:
            return redirect(reverse("product-card", kwargs={"pk": self._product_id}))

        return super(ProductsView, self).render_to_response(context=context, **response_kwargs)

    def _add_multiple_url_filtring_args(self, filters: dict) -> None:
        multiple_url_filtering_args = {
            multiple_url_arg: self.request.GET.get(multiple_url_arg)
            for multiple_url_arg in self._MULTIPLE_VALUES_URL_ARGS
        }

        for multiple_url_filtering_arg in multiple_url_filtering_args:
            if not multiple_url_filtering_args[multiple_url_filtering_arg]:
                continue

            try:
                choises = [
                    self._CHOISES_VALUES_FOR_CODES_FOR_FIELD[multiple_url_filtering_arg][
                        int(url_filtering_arg) if url_filtering_arg.isdigit() else url_filtering_arg
                    ] for url_filtering_arg in self.request.GET.getlist(multiple_url_filtering_arg)
                ]
            except KeyError:
                continue

            filters.update({f"phone__{multiple_url_filtering_arg}__in": choises})

    def _get_queryset(self, category: str, **query_filters) -> QuerySet:
        queryset: QuerySet = category_model_services.get_categories_queryset(
            parent_category=category, ordering=self._ordering_field, **query_filters
        )

        if not queryset.count():
            queryset: QuerySet = phone_model_services.get_phones_queryset(
                category=category, ordering=self._ordering_field,
                **convert_category_filters_to_product_filters(query_filters=query_filters),
            )

            if queryset.count() == 1:
                self._product_id = queryset.first().pk

        return queryset

    def _complement_context(self, current_context: dict) -> None:
        price_range_bounds = services_utils.get_product_prices_bounds(
            request_get_args=self.request.GET, max_price_bound=self._max_product_price
        )

        filters_window_displayed = services_utils.filters_window_requested(request_get_args=self.request.GET)

        url_arguments = dict(
            price=urls_services.get_url_arg_from_ordering_field(field=self._ordering_field),
            min_=price_range_bounds[0],
            filters=filters_window_displayed,
            max_=price_range_bounds[1],
            **{multiple_url_arg: self.request.GET.getlist(multiple_url_arg)
               for multiple_url_arg in self._MULTIPLE_VALUES_URL_ARGS}
        )

        current_context.update(dict(
            filters=filters_window_displayed,
            price_bounds=price_range_bounds,
            max_item_price=self._max_product_price,
            category_name=self.kwargs.get("category"),
            url_args=urls_services.compile_url_args(**url_arguments),
            url_args_invert_sorting=urls_services.compile_inverted_price_url_args(**url_arguments),
            **{f"supported_{multiple_url_arg}s": self._CHOISES_LIST_FOR_FIELD[multiple_url_arg]
               for multiple_url_arg in self._MULTIPLE_VALUES_URL_ARGS}
        ))

        if any(self.request.GET.getlist(multiple_url_arg) for multiple_url_arg in self._MULTIPLE_VALUES_URL_ARGS):
            for url_multiple_arg_name in self._MULTIPLE_VALUES_URL_ARGS:
                current_context.update({f"selected_{url_multiple_arg_name}_values": tuple(
                    int(url_value) if url_value.isdigit() else url_value
                    for url_value in self.request.GET.getlist(url_multiple_arg_name)
                )})

    def _set_ordering_field(self, request: WSGIRequest):
        self._ordering_field = urls_services.get_ordering_field_from_url_arg(
            url_arg=request.GET.get("price"), field="price"
        )

    def _set_max_product_price(self) -> None:
        self._max_product_price = phone_model_services.get_max_phone_price()


class ProductDetailView(DetailView):
    model = Phone
    template_name = "products/product-details.html"
    context_object_name = "item_info"

    object: BaseProduct
    __card_viewer_is_owner: bool = None

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update(dict(
            viewer_is_author=self._card_viewer_is_owner,
            storage=current_context["item_info"].get_storage_display(),
        ))

        return current_context

    def render_to_response(self, context, **response_kwargs):
        if not context["viewer_is_author"] and self.object.products_count < 1:
            return HttpResponseRedirect(redirect_to=reverse("product-not-exist"))

        if not self._card_viewer_is_owner:
            increment_product_views(phone=self.object)

        return super().render_to_response(context=context, **response_kwargs)

    @property
    def _card_viewer_is_owner(self) -> bool:
        if not self.__card_viewer_is_owner:
            self.__card_viewer_is_owner = (self.request.__dict__.get("user") and
                                           self.request.user == self.object.author)

        return self.__card_viewer_is_owner


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
            target_category, _ = Category.objects.get_or_create(
                title=spaces_to_dashes(form.instance.title),
                defaults=dict(parent=form.instance.category, photo=form.instance.photo)
            )
        except ValidationError:
            return super().form_invalid(form=form)

        form.instance.category = target_category

        return super().form_valid(form=form)


class EditProductView(AddProductView):
    form_class = EditProductForm

    _current_product: Phone = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if not self._current_product:
            self._current_product = self.object or self.get_object()

        kwargs['instance'] = self._current_product
        kwargs['instance'].title = kwargs['instance'].readable_title()

        return kwargs

    def get_context_data(self, **kwargs):
        current_context = super().get_context_data(**kwargs)

        current_context.update({"current_product": self._current_product})

        return current_context


class DeleteUserProductView(UserLoginRequiredMixin, DeleteView):
    model = Phone
    object: Phone

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return self.form_valid(form=None)

    def get_success_url(self):
        return reverse("account-products", kwargs={"pk": self.request.user.id})

    def get_object(self, queryset=None) -> BaseProduct:
        return self.model.objects.get(pk=self.kwargs.get("pk"), author=self.request.user)


class ProductDoesNotExistWarningView(UserLoginRequiredMixin, TemplateView):
    template_name = "products/product-does-not-exist.html"
