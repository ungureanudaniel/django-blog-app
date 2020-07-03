from .models import Subscribe
from django import forms


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Subscribe
        fields = ['email', 'name']

        widgets = {
            'email': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add your email please...'}),
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add full name please...'}),
        }
