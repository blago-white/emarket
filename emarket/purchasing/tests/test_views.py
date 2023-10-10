from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.test.client import RequestFactory
from django.urls import reverse
from emarket.testsutils import tests_presets
from emarket.testsutils import tests_utils

from products.models.models import Phone
from users.models.models import Notifications
from ..models import ShoppingBasket
from ..views import ShoppingBasketView, DeleteProductFromBasketView, AddProductToBasketView, BuyProductView


class _BaseShoppingBasketViewTestCase(tests_presets.BaseSingleUserTestCase):
    TEST_PRODUCT_COUNT = 2
    request_factory: RequestFactory
    test_user: User
    test_product: Phone
    test_product_basket: ShoppingBasket

    def setUp(self) -> None:
        super().setUp()

        self.test_product = tests_utils.create_test_product(test_user=self.test_user,
                                                            products_count=self.TEST_PRODUCT_COUNT)

    def add_test_product_to_basket(self, target_user: User) -> None:
        self.test_product_basket = ShoppingBasket(user=target_user, product=self.test_product)
        self.test_product_basket.save()


class ShoppingBasketViewTestCase(_BaseShoppingBasketViewTestCase):
    def test_get_context_data(self):
        basket_view_request = self.get_request_with_test_user(request_method=self.request_factory.get,
                                                              path=reverse("basket")
                                                              )

        basket_view_response = ShoppingBasketView.as_view()(basket_view_request)

        self.assertTrue(basket_view_response.context_data["is_self_account"])
        self.assertEqual(basket_view_response.context_data["current_section"], "basket")

    def test_get_queryset(self):
        basket_view_request = self.get_request_with_test_user(request_method=self.request_factory.get,
                                                              path=reverse("basket"))

        super().add_test_product_to_basket(target_user=self.test_user)

        basket_view_response = ShoppingBasketView.as_view()(basket_view_request)

        self.assertEqual(basket_view_response.context_data["products"].count(), 1)
        self.assertEqual(basket_view_response.context_data["products"][0].product, self.test_product)
        self.assertEqual(basket_view_response.context_data["products"][0].user, self.test_user)


class DeleteProductFromBasketViewTestCase(_BaseShoppingBasketViewTestCase):
    def test_get_object(self):
        self.add_test_product_to_basket(target_user=self.test_user)

        request = self.get_request_with_test_user(request_method=self.request_factory.post,
                                                  path=reverse("delete-basket-product",
                                                               kwargs={"pk": self.test_product_basket.id}
                                                               )
                                                  )

        DeleteProductFromBasketView.as_view()(request, pk=self.test_product_basket.id)

        with self.assertRaises(ShoppingBasket.DoesNotExist):
            ShoppingBasket.objects.get(product=self.test_product)


class AddProductToBasketViewTestCase(_BaseShoppingBasketViewTestCase):
    _second_test_user: User

    def setUp(self) -> None:
        super().setUp()
        self._second_test_user = tests_utils.create_test_user()

    def test_form_invalid(self):
        self.assertTrue(tests_utils.response_is_redirect(AddProductToBasketView().form_invalid(form=None)))

    def test_form_valid(self):
        self._test_add_self_product()
        self._test_add_product()

    def _test_add_product(self):
        add_product_to_basket_request = self._get_test_add_product_to_basket_request(target_user=self._second_test_user)

        AddProductToBasketView.as_view()(add_product_to_basket_request, productid=self.test_product.id)

        added_to_basket_product: ShoppingBasket = ShoppingBasket.objects.get(product=self.test_product)

        self.assertEqual(added_to_basket_product.user, self._second_test_user)
        self.assertEqual(added_to_basket_product.product, self.test_product)

    def _test_add_self_product(self):
        add_product_to_basket_request = self._get_test_add_product_to_basket_request(target_user=self.test_user)

        add_product_canceled_request: HttpResponseRedirect = AddProductToBasketView.as_view()(
            add_product_to_basket_request, productid=self.test_product.id
        )

        self.assertTrue(tests_utils.response_is_redirect(add_product_canceled_request))

        with self.assertRaises(ShoppingBasket.DoesNotExist):
            ShoppingBasket.objects.get(product=self.test_product)

    def _get_test_add_product_to_basket_request(self, target_user: User) -> WSGIRequest:
        add_product_to_basket_request = self.request_factory.post(
            reverse("save-product", kwargs={"productid": self.test_product.id})
        )
        add_product_to_basket_request.user = target_user

        return add_product_to_basket_request


class BuyProductViewTestCase(_BaseShoppingBasketViewTestCase):
    ORDINARY_ORDER_NOTIFICATIONS_THEMES = {"owner": ["pur"], "purchaser": ["inf"]}
    LAST_PRODUCT_ORDER_NOTIFICATIONS_THEMES = {"owner": ["inf", "pur"], "purchaser": ["inf"]}
    SOLDOUTED_PRODUCT_ORDER_NOTIFICATIONS_THEMES = {"owner": [], "purchaser": []}

    _second_test_user: User
    _expected_test_product_count: int = _BaseShoppingBasketViewTestCase.TEST_PRODUCT_COUNT

    def setUp(self) -> None:
        super().setUp()
        self._second_test_user = tests_utils.create_test_user()
        self.add_test_product_to_basket(target_user=self._second_test_user)

    def test_form_valid(self):
        self._test_order_product(self.ORDINARY_ORDER_NOTIFICATIONS_THEMES)
        self._test_order_product(self.LAST_PRODUCT_ORDER_NOTIFICATIONS_THEMES)
        self._test_order_product(self.SOLDOUTED_PRODUCT_ORDER_NOTIFICATIONS_THEMES)

    def _test_order_product(self, expected_notifications_themes_set_after_order: dict[str, list[str | None]]):
        self._buy_product_from_basket_using_view()

        self._test_notifications_after_order(
            expected_notifications_themes_set_after_order=expected_notifications_themes_set_after_order
        )

        self._decrease_expected_test_product_count()
        self._test_products_count_after_order(expected_products_count=self._expected_test_product_count)

        self._recover_tables_after_order()

    def _test_notifications_after_order(self, expected_notifications_themes_set_after_order: dict[str, list[str | None]]):
        owner_notifications_themes, purchaser_notifications_themes = (
            _get_test_user_notifications_themes(test_user=self.test_user),
            _get_test_user_notifications_themes(test_user=self._second_test_user)
        )

        self.assertEqual(sorted(expected_notifications_themes_set_after_order["owner"]),
                         owner_notifications_themes)
        self.assertEqual(sorted(expected_notifications_themes_set_after_order["purchaser"]),
                         purchaser_notifications_themes)

    def _get_test_buy_product_request(self, target_user: User) -> WSGIRequest:
        buy_product_request = self.request_factory.post(
            reverse("buy-product", kwargs={"pk": self.test_product_basket.id})
        )
        buy_product_request.user = target_user

        return buy_product_request

    def _buy_product_from_basket_using_view(self):
        BuyProductView.as_view()(
            self._get_test_buy_product_request(target_user=self._second_test_user), pk=self.test_product_basket.id
        )

    def _recover_tables_after_order(self):
        ShoppingBasket.objects.all().delete()
        self.add_test_product_to_basket(target_user=self._second_test_user)
        Notifications.objects.all().delete()

    def _test_products_count_after_order(self, expected_products_count: int) -> None:
        self.assertEqual(Phone.objects.get(pk=self.test_product.id).products_count, expected_products_count)

    def _decrease_expected_test_product_count(self):
        self._expected_test_product_count = max(self._expected_test_product_count-1, 0)


def _get_test_user_notifications_themes(test_user: User) -> list[str]:
    return sorted([
            i["theme"] for i in Notifications.objects.filter(recipient=test_user).values("theme")
    ])
