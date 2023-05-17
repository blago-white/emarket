from django.core.validators import RegexValidator

category_name_validator = RegexValidator(r'^[a-z ]*$', 'Only lower alphabet characters are allowed.')
