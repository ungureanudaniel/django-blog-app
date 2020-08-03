from django import forms
from .models import Subscribe
from django.contrib.auth import (
    login,
    logout
)

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"type": "email", "name": "email", "id": "email", "placeholder": "Add your email please..."}), label="")
    class Meta:
        model = Subscribe
        fields = ['email']

        # def clean_email(self):
        #     email = self.cleaned_data.get()
        #
        #     return email