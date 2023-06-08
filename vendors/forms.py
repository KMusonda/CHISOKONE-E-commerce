from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . models import Vendor


# Create your forms here.
class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = Vendor
        widgets = {
            'password': forms.PasswordInput(),
		}
        fields = ("name","password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        if commit:
            user.save()
        return user