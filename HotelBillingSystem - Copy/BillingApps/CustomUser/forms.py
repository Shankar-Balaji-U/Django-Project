from django import forms
from CustomUser.models import CustomUser
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class CustomUserAdminForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('__all__')


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder':'Enter your e-mail id', 'autocomplete':'off'}),)
    password1 = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}),
            label=_('Password'), help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder':'Re-enter your password'}),
            label=_('Confirm Password'), help_text=_("Enter the same password as before, for verification."),)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder':'Enter your e-mail id', 'autocomplete':'off'}),)
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}), )

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # class Meta:
    #     widgets = {
    #         'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'name@example.com', 'autocomplete':'off'})
    #     }