from django import forms
from django.contrib.auth.models import User
from .models import Customer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # check that email is not duplicate
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email


class CustomerUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ['user',]