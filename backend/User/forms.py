from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name:"
        self.fields['last_name'].label = "Last Name:"
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Confirm Password:"
        self.fields['email'].label = "Email(Req):"

        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'Enter First Name'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Enter Last Name'}
        )
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter Email'}
        )
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Enter Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Confirm Password'}
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    
    email =  forms.EmailField(widget=forms.EmailInput(attrs={ 'placeholder':'Email',})) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
    }))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")


        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user