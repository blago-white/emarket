from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

username_min_length_validator = MinLengthValidator(limit_value=3, message="Username must be longer")

username_max_length_validator = MaxLengthValidator(limit_value=25, message="Username must be shorter")

username_letters_validator = RegexValidator(r'^[A-Za-z -]*$', 'Only alphabet characters, dashes and spaces are allowed.')

