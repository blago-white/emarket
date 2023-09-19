from django.core.validators import RegexValidator

__all__ = ["card_title_validator", "child_category_title_validator", "parent_category_title_validator"]

card_title_validator = RegexValidator(r"^[a-zA-Z0-9 ]*$",
                                      "Only alphabet characters, spaces and digits are allowed.")

parent_category_title_validator = RegexValidator(r"^[a-z0-9 ]*$",
                                                 "Only lower alphabet characters and spaces are allowed.")

child_category_title_validator = card_title_validator
