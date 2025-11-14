from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form to create a new user with role selection (buyer or dealer).
    """
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('dealer', 'Dealer'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='buyer',
        help_text="Select if you are a buyer or dealer"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form to authenticate existing users.
    """
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)
