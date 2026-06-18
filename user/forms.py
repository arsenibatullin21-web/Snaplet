from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.password_validation import validate_password


class UserLoginForm(AuthenticationForm):
    username = UsernameField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    username = UsernameField(required=True)
    password1 = forms.CharField(required=True, validators=[validate_password, ])
    password2 = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'phone']

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
