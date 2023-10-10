from django.conf import settings

__all__ = ["PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE",
           "PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE",
           "PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE",
           "PURCHASE_MESSAGE_FOR_OWNER_HTML_TEMPLATE",
           "PURCHASE_MESSAGE_FOR_PURCHASER_HTML_TEMPLATE",
           "PRODUCT_IS_OVER_WARNING_MESSAGE_HTML_TEMPLATE"]

with open(settings.BASE_DIR / "purchasing/notifications_templates/base-email-notification.html", "r") as email_text:
    _BASE_HTML_EMAIL_NOTIFICATION_TEXT = "".join(email_text.readlines())


def _complement_base_html_notification_text(template_name: str) -> str:
    with open(settings.BASE_DIR / ("purchasing/notifications_templates/" + template_name), "r") as email_text:
        return _BASE_HTML_EMAIL_NOTIFICATION_TEXT.format("".join(email_text.readlines()))


PURCHASE_MESSAGE_FOR_OWNER_HTML_TEMPLATE = _complement_base_html_notification_text(
    template_name="purchase_message_for_owner_html_template.html"
)

PURCHASE_MESSAGE_FOR_PURCHASER_HTML_TEMPLATE = _complement_base_html_notification_text(
    template_name="purchase_message_for_purchaser_html_template.html"
)

PRODUCT_IS_OVER_WARNING_MESSAGE_HTML_TEMPLATE = _complement_base_html_notification_text(
    template_name="product_is_over_warning_message_html_template.html"
)

PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE = """
    User {username}({usermail}) ordered the {productname} for the price of {price}
"""
PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE = """
    You ordered the {productname} for the price of {price}, if owner {username}({usermail}) will approve the purchase,
     he send mail for you
"""
PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE = """
    The product {productname} has ended, now it will NOT BE DISPLAYED to users, if you have new units of goods, 
    change the corresponding field (products count)
"""
