from django.test import TestCase
from django.http.request import HttpRequest

from users.models.models import DistributionDeliveredMessage
from users.filters import *


class _IPDependedFiltersTestCaseMixin:
    _TEST_IP = "0.0.0.0"

    def _get_test_request(self) -> HttpRequest:
        return HttpRequest()


class FiltersTestCase(TestCase):
    maxDiff = None
    _test_wrap_stmts = ((0, ("", )),
                        (1, ("l"*18, "l")),
                        (2, ("l"*19, "l"*36)))
    _test_enumerate_sequences = ((1, 2, 3),
                                 {1, 2, 3},
                                 [1, 2, 3],
                                 [])

    def test_wrap(self) -> None:
        for goal_length, stmts in self._test_wrap_stmts:
            for stmt in stmts:
                self.assertEqual(len(wrap(stmt)), goal_length)

    def test_enumerate_(self) -> None:
        for test_sequence in self._test_enumerate_sequences:
            self.assertEqual(tuple(enumerate_(test_sequence)), tuple(enumerate(test_sequence)))

    def test_get_title_theme(self) -> None:
        self.assertEqual(get_title_theme(name="inf"), "info")
        self.assertEqual(get_title_theme(name="pur"), "purchase")
        self.assertEqual(get_title_theme(name="none"), None)


class ShowNotificationForUserTestCase(_IPDependedFiltersTestCaseMixin, TestCase):
    _TEST_RELEVANT_PATH = "/"


    def test_show_notication_for_user(self):
        self.assertFalse(show_notication_for_user(request=self._get_test_irrelevant_request()))

        test_relevant_request = self._get_test_relevant_for_notification_request()

        self.assertTrue(show_notication_for_user(request=test_relevant_request))

        self._set_notification_delivered_for_ip()

        self.assertFalse(show_notication_for_user(request=test_relevant_request))

    def _set_notification_delivered_for_ip(self) -> None:
        DistributionDeliveredMessage(ip=self._TEST_IP).save()

    def _get_test_relevant_for_notification_request(self) -> HttpRequest:
        test_relevant_request = self._get_test_irrelevant_request()

        test_relevant_request.path = self._TEST_RELEVANT_PATH

        return test_relevant_request

    def _get_test_irrelevant_request(self) -> HttpRequest:
        return self._get_test_request()

    def _get_test_request(self) -> HttpRequest:
        test_request = super()._get_test_request()

        test_request.META.update(REMOTE_ADDR=self._TEST_IP)

        return test_request


class GetUserIPFromRequestTestCase(_IPDependedFiltersTestCaseMixin, TestCase):
    def test_get_user_ip_from_request(self):
        test_request = self._get_test_request()

        self.assertIsNone(get_user_ip_from_request(test_request))

        self.assertIsNone(get_user_ip_from_request(None))

        self._set_remote_addr_header(test_request=test_request, ip=self._TEST_IP)

        self.assertEqual(get_user_ip_from_request(test_request), self._TEST_IP)

        self._set_forwarded_for_header(test_request=test_request, ip=self._TEST_IP)

        self.assertEqual(get_user_ip_from_request(test_request), self._TEST_IP)

    def _get_test_request(self) -> HttpRequest:
        test_request = super()._get_test_request()

        return test_request

    @staticmethod
    def _set_forwarded_for_header(test_request: HttpRequest, ip: str):
        test_request.META.update(HTTP_X_FORWARDED_FOR=ip)

    @staticmethod
    def _set_remote_addr_header(test_request: HttpRequest, ip: str):
        test_request.META.update(REMOTE_ADDR=ip)
