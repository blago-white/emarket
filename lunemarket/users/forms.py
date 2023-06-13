from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import django.forms as forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="username")
    email = forms.CharField(label="email adress")
    password1 = forms.CharField(label="password")
    password2 = forms.CharField(label="repeat password")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This e-mail is already registered')
        return email
