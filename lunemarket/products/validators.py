from django.core.validators import RegexValidator

category_title_validator = RegexValidator(r'^[a-z ]*$', 'Only lower alphabet characters and spaces are allowed.')

card_title_validator = RegexValidator(r'^[a-zA-Z0-9 ]*$', 'Only alphabet characters, spaces and digits are allowed.')

duplicate_spaces_validator = RegexValidator(r'  |[^\\p{L}_ -]', 'Repetition of spaces is not allowed')
