from django.core.handlers.wsgi import WSGIRequest
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from products.models.models import Category, Phone

__all__ = ["TEST_USER_DEFAULT_PASSWORD",
           "TEST_USER_DEFAULT_USERNAME",
           "TEST_USER_DEFAULT_EMAIL",
           "TEST_SECOND_USER_DEFAULT_USERNAME",
           "TEST_PHONE_DEFAULT_FIELDS",
           "TEST_CATEGORY_DEFAULT_FIELDS",
           "BaseViewTestCaseWithRequests",
           "BaseSingleUserTestCase",
           "BaseTwinUsersTestCase"]

TEST_USER_DEFAULT_PASSWORD = "testPASSword123@SSSSS"
TEST_USER_DEFAULT_EMAIL = "example@example.com"
TEST_USER_DEFAULT_USERNAME = "testusername"
TEST_SECOND_USER_DEFAULT_USERNAME = "testusername_"

TEST_PHONE_DEFAULT_FIELDS = dict(
    title="test-phone",
    category=None,
    photo="test-photo.jpg",
    price=100,
    views=0,
    products_count=1,
    author=None,
    color="#222222",
    stortage=1
)
TEST_CATEGORY_DEFAULT_FIELDS = dict(
    title="testcategory",
    photo="test-photo.jpg"
)


class BaseViewTestCaseWithRequests(TestCase):
    request_factory: RequestFactory = RequestFactory()


class BaseSingleUserTestCase(BaseViewTestCaseWithRequests):
    test_user: User

    def setUp(self) -> None:
        self.test_user = User(username=TEST_USER_DEFAULT_USERNAME, password=TEST_USER_DEFAULT_PASSWORD)
        self.test_user.save()

    def get_request_with_test_user(
            self, request_method,
            path: str, **request_data) -> WSGIRequest:
        request: WSGIRequest = request_method(path, data={**request_data})
        request.user = self.test_user

        return request


class BaseTwinUsersTestCase(BaseViewTestCaseWithRequests):
    first_test_user: User
    second_test_user: User

    def setUp(self) -> None:
        self.first_test_user, self.second_test_user = (
            User(username=TEST_USER_DEFAULT_USERNAME,
                 password=TEST_USER_DEFAULT_PASSWORD,
                 email="example1@example.com"),
            User(username=TEST_SECOND_USER_DEFAULT_USERNAME,
                 password=TEST_USER_DEFAULT_PASSWORD,
                 email="example2@example.com"),
        )

        self.first_test_user.save()
        self.second_test_user.save()

    def get_request_with_first_user(
            self, request_method,
            path: str, **request_data) -> WSGIRequest:
        request: WSGIRequest = request_method(path, data={**request_data})
        request.user = self.first_test_user

        return request

    def get_request_with_second_user(
            self, request_method,
            path: str, **request_data) -> WSGIRequest:
        request: WSGIRequest = request_method(path, data={**request_data})
        request.user = self.second_test_user

        return request
