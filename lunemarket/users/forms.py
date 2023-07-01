import django.forms as forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models.models import UserProfile


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="email adress")
    password1 = forms.CharField(label="password")
    password2 = forms.CharField(label="repeat password")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email, username = self.cleaned_data.get('email'), self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("This e-mail is already exists")

        return email


class ChangeUsernameForm(forms.ModelForm):
    username = forms.CharField(label="new username",
                               widget=forms.TextInput(
                                   attrs={"style": "text-align: center;",
                                          "class": "username-input"}
                               ))

    class Meta:
        model = User
        fields = ("username",)


class ChangeEmailForm(forms.ModelForm):
    email = forms.CharField(label="new username",
                            widget=forms.EmailInput(
                                attrs={"style": "text-align: center;",
                                       "class": "username-input"}
                            ))

    class Meta:
        model = User
        fields = ("email",)


class ChangeAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label="new username", required=True, widget=forms.FileInput())

    class Meta:
        model = UserProfile
        fields = ("avatar",)
