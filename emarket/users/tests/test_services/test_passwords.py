from emarket.testsutils.tests_presets import BaseSingleUserTestCase
from users.services import passwords


class PasswordsServiceTestCase(BaseSingleUserTestCase):
    def test_get_reset_password_request(self):
        reset_password_request = passwords.get_reset_password_request(user=self.test_user)
        self.assertEqual(reset_password_request.POST.get("email"), self.test_user.email)
