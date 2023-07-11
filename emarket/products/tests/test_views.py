from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.core.files.uploadedfile import SimpleUploadedFile

from emarket.testsutils.tests_presets import (BaseSingleUserTestCase,
                                                    BaseTwinUsersTestCase,
                                                    TEST_CATEGORY_DEFAULT_FIELDS,
                                                    TEST_PHONE_DEFAULT_FIELDS)
from emarket.testsutils import tests_utils

from ..filters import dashes_to_spaces, spaces_to_dashes
from ..models.models import Category, Phone
from ..views import (ProductsView,
                     ProductDetailView,
                     DeleteUserProductView,
                     AddProductView,
                     EditProductView,
                     HomePageProductsView)


class ProductsViewTestCase(BaseSingleUserTestCase):
    _test_products: list[Phone]
    _test_category: Category

    def setUp(self) -> None:
        super().setUp()
        self._test_category = tests_utils.create_default_test_category()

    def test_get_queryset(self):
        self._test_get_queryset()

    def _test_get_queryset(self):
        self._test_get_queryset_without_products()
        self._create_products_for_category()
        self._test_get_queryset_products()

    def _test_get_queryset_products(self):
        self._test_get_filtered_queryset()

        products_view_response: TemplateResponse = ProductsView.as_view()(
            self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]})
            ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
        )
        self.assertTrue(products_view_response.context_data["items"].exists())

    def _test_get_filtered_queryset(self):
        self._test_queryset_ordering()
        self._test_queryset_prices_range()
        self._test_queryset_stortage_filter()
        self._test_queryset_color_filter()
        self._test_queryset_null_products_count()

    def _test_get_queryset_without_products(self):
        products_view_response: TemplateResponse = ProductsView.as_view()(
            self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]})
            ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
        )
        self.assertFalse(products_view_response.context_data["items"].exists())

    def _test_queryset_ordering(self):
        products_view_response: TemplateResponse = ProductsView.as_view()(
            self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) + "?price=0"
            ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
        )
        self.assertEqual(tuple(products_view_response.context_data["items"]),
                         tuple(Phone.objects.all().reverse()))

    def _test_queryset_prices_range(self):
        products_view_response: TemplateResponse = ProductsView.as_view()(
            self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) + "?max=1501"
            ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
        )

        self.assertEqual(tuple(products_view_response.context_data["items"]),
                         tuple(Phone.objects.filter(price__lt=1501)))

        self.assertEqual(tuple(
            ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products",
                            kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) + "?max=n"
                ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            ).context_data["items"]
        ), tuple(Phone.objects.all()))

        self.assertTrue(tests_utils.response_is_redirect(
            ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                    "?max=1501&min=900"
                ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            )
        ))

        self.assertTrue(tests_utils.response_is_redirect(
            ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                    "?max=900&min=1501"
                ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            )
        ))

    def _test_queryset_color_filter(self):
        self.assertEqual(
            tuple(ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                    "?stortage=256"
                ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]).context_data["items"]),
            tuple(Phone.objects.filter(stortage=3)))

        self.assertFalse(
            ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                    "?stortage=0"
                ), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]).context_data["items"].exists()
        )

    def _test_queryset_stortage_filter(self):
        self.assertEqual(
            tuple(ProductsView.as_view()(self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                "?stortage=256"), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            ).context_data["items"]),
            tuple(Phone.objects.filter(stortage=3))
        )

        self.assertFalse(
            ProductsView.as_view()(
                self.request_factory.get(
                    reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]}) +
                    "?stortage=0"), category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            ).context_data["items"].exists()
        )

    def _test_queryset_null_products_count(self):
        self._create_test_phone_with_null_products_count()
        self.assertEqual(
            tuple(ProductsView.as_view()(self.request_factory.get(
                reverse("category-products", kwargs={"category": TEST_CATEGORY_DEFAULT_FIELDS["title"]})),
                category=TEST_CATEGORY_DEFAULT_FIELDS["title"]
            ).context_data["items"]),
            tuple(Phone.objects.filter(products_count__gt=0))
        )

    def _create_test_phone_with_null_products_count(self):
        tests_utils.create_test_product(test_user=self.test_user,
                                        category=self._test_category,
                                        title="test-phone-null-count",
                                        products_count=0)

    def _create_products_for_category(self):
        test_products = [
            tests_utils.create_test_product(test_user=self.test_user, test_category=self._test_category),
        ]
        custom_test_products = [
            Phone(title="test-phone-second",
                  category=self._test_category,
                  photo="test-photo.jpg",
                  price=1500,
                  views=1,
                  products_count=1,
                  author=self.test_user,
                  color="#E4717A",
                  stortage=3),
            Phone(title="test-phone-third",
                  category=self._test_category,
                  photo="test-photo.jpg",
                  price=2000,
                  views=1,
                  products_count=1,
                  author=self.test_user,
                  color="#E4717A",
                  stortage=3)
        ]

        for custom_phone in custom_test_products:
            custom_phone.save()

        self._test_products = test_products + custom_test_products


class ProductDetailViewTestCase(BaseTwinUsersTestCase):
    _test_product: Phone

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.first_test_user)

    def test_get_object(self):
        self._test_increment_views()

    def test_get_context_data(self):
        self._test_viewer_is_author_context()
        self._test_phone_stortage_display()

    def _test_phone_stortage_display(self):
        self.assertEqual(
            ProductDetailView.as_view()(
                self.request_factory.get(reverse("product-card", kwargs={"pk": self._test_product.id})),
                pk=self._test_product.id).context_data.get("stortage"),
            self._test_product.get_stortage_display()
        )

    def _test_viewer_is_author_context(self):
        self.assertTrue(
            ProductDetailView.as_view()(
                self.get_request_with_first_user(request_method=self.request_factory.get,
                                                 path=reverse("product-card", kwargs={"pk": self._test_product.id})),
                pk=self._test_product.id).context_data.get("viewer_is_author")
        )
        self.assertFalse(
            ProductDetailView.as_view()(
                self.get_request_with_second_user(request_method=self.request_factory.get,
                                                  path=reverse("product-card", kwargs={"pk": self._test_product.id})),
                pk=self._test_product.id).context_data.get("viewer_is_author")
        )
        self.assertFalse(ProductDetailView.as_view()(
            self.request_factory.get(reverse("product-card", kwargs={"pk": self._test_product.id})),
            pk=self._test_product.id).context_data.get("viewer_is_author")
                         )

    def _test_increment_views(self):
        ProductDetailView.as_view()(
            self.get_request_with_first_user(request_method=self.request_factory.get,
                                             path=reverse("product-card", kwargs={"pk": self._test_product.id})),
            pk=self._test_product.id
        )
        ProductDetailView.as_view()(
            self.get_request_with_second_user(request_method=self.request_factory.get,
                                              path=reverse("product-card", kwargs={"pk": self._test_product.id})),
            pk=self._test_product.id
        )
        ProductDetailView.as_view()(
            self.request_factory.get(reverse("product-card", kwargs={"pk": self._test_product.id})),
            pk=self._test_product.id
        )

        self.assertEqual(Phone.objects.get(pk=self._test_product.id).views, self._test_product.views + 2)


class DeleteUserProductViewTestCase(BaseTwinUsersTestCase):
    _test_product: Phone

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.first_test_user)

    def test_get_object(self):
        test_delete_product_view = DeleteUserProductView()
        test_delete_product_view.kwargs = {"pk": self._test_product.id}

        self.assertRaises(AttributeError, test_delete_product_view.get_object)

        test_delete_product_view.request = self.get_request_with_second_user(
            request_method=self.request_factory.post,
            path=reverse("delete-product", kwargs={"pk": self._test_product.id})
        )

        self.assertRaises(Phone.DoesNotExist, test_delete_product_view.get_object)

        test_delete_product_view.request = self.get_request_with_first_user(
            request_method=self.request_factory.post,
            path=reverse("delete-product", kwargs={"pk": self._test_product.id})
        )

        self.assertEqual(test_delete_product_view.get_object(), self._test_product)

    def test_get_succes_url(self):
        with self.assertRaises(AttributeError):
            DeleteUserProductView.as_view()(
                self.request_factory.post(reverse("delete-product", kwargs={"pk": self._test_product.id})),
                pk=self._test_product.id
            )

        with self.assertRaises(Phone.DoesNotExist):
            DeleteUserProductView.as_view()(
                self.get_request_with_second_user(
                    request_method=self.request_factory.post,
                    path=reverse("delete-product", kwargs={"pk": self._test_product.id})
                ),
                pk=self._test_product.id
            )

        success_delete_response: HttpResponseRedirect = DeleteUserProductView.as_view()(
            self.get_request_with_first_user(
                request_method=self.request_factory.post,
                path=reverse("delete-product", kwargs={"pk": self._test_product.id})
            ),
            pk=self._test_product.id
        )

        self.assertTrue(tests_utils.response_is_redirect(success_delete_response))
        self.assertEqual(success_delete_response.headers["Location"],
                         reverse("account-products", kwargs={"pk": self.first_test_user.id}))


class AddProductViewTestCase(BaseSingleUserTestCase):
    _TEST_PRODUCT_FIELDS_VALID: dict
    _TEST_PRODUCT_FIELDS_INVALID: dict

    def setUp(self) -> None:
        super().setUp()
        self._TEST_PRODUCT_FIELDS_VALID = _get_test_product_form_fields()
        self._TEST_PRODUCT_FIELDS_INVALID = _get_test_product_form_invalid_fields(self._TEST_PRODUCT_FIELDS_VALID)

    def test_add_product(self):
        self._test_add_product_invalid()
        self._test_add_product_success()

    def _test_add_product_invalid(self):
        test_add_product_response = self._get_add_product_view_response(**self._TEST_PRODUCT_FIELDS_INVALID)

        self.assertFalse(Phone.objects.all().exists())
        self.assertIsInstance(test_add_product_response, TemplateResponse)
        self.assertTrue("error_class" in test_add_product_response.context_data["form"].__dict__)

    def _test_add_product_success(self):
        test_add_product_response = self._get_add_product_view_response(**self._TEST_PRODUCT_FIELDS_VALID)

        created_phone = Phone.objects.all()[0]

        self.assertTrue(tests_utils.response_is_redirect(test_add_product_response))
        self.assertEqual(created_phone.author, self.test_user)
        self.assertEqual(created_phone.category.title, spaces_to_dashes(self._TEST_PRODUCT_FIELDS_VALID["title"]))
        self.assertEqual(created_phone.category.parent.title, TEST_CATEGORY_DEFAULT_FIELDS["title"])

    def _get_add_product_view_response(self, **add_product_form_fields: dict) -> HttpResponse:
        return AddProductView.as_view()(
            self.get_request_with_test_user(request_method=self.request_factory.post,
                                            path=reverse("add-product"),
                                            **add_product_form_fields)
        )


class EditProductViewTestCase(BaseSingleUserTestCase):
    _test_product: Phone

    def setUp(self) -> None:
        super().setUp()
        self._test_product = tests_utils.create_test_product(test_user=self.test_user)

    def test_get_form_kwargs(self):
        test_edit_product_response = EditProductView.as_view()(
            self.get_request_with_test_user(request_method=self.request_factory.get,
                                            path=reverse("edit-product", kwargs={"pk": self._test_product.id})),
            pk=self._test_product.id
        )

        self.assertIsInstance(test_edit_product_response, TemplateResponse)
        self.assertEqual(test_edit_product_response.context_data["form"].initial["title"],
                         self._test_product.readable_title())


class HomePageProductsViewTestCase(BaseSingleUserTestCase):
    def test_get_queryset(self):
        self.assertEqual(tuple(HomePageProductsView().get_queryset()), tuple(Category.objects.filter(parent=None)))


def _get_test_product_form_fields() -> dict:
    test_product_form_fields = TEST_PHONE_DEFAULT_FIELDS.copy()

    test_product_form_fields["title"] = dashes_to_spaces(test_product_form_fields["title"])
    test_product_form_fields["category"] = tests_utils.create_default_test_category()
    test_product_form_fields["photo"] = _get_test_image()

    del test_product_form_fields["author"], test_product_form_fields["views"]

    return test_product_form_fields


def _get_test_product_form_invalid_fields(valid_fields: dict) -> dict:
    unvalid_fields = valid_fields.copy()

    unvalid_fields["photo"] = str()

    return unvalid_fields


def _get_test_image() -> SimpleUploadedFile:
    return SimpleUploadedFile(name='test_image.jpg',
                              content=open(_get_test_image_path(), 'rb').read(),
                              content_type='image/jfif')


def _get_test_image_path() -> str:
    return "C:\\Users\\GAME-X\\Desktop\\iam.jfif"
