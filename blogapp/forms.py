from django import forms
from .models import Category, Post, About

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'text', 'category', 'seo_title', 'seo_description', 'created_date', 'updated_date']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title...'}),
            'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title tag...'}),
            'author': forms.TextInput(attrs = {'class': 'form-control', 'value': '', 'id':'ioana', 'type':'hidden'}),
            'category': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            'text' : forms.Textarea(attrs = {'class': 'form-control'}),
            'seo_title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title seo...'}),
            'seo_description': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a description seo...'}),
            'status': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            #'published_date': forms.DateField(attrs = {'class': 'form-control'}),
            #'created_date': forms.DateField(attrs = {'class': 'form-control'}),
        }

class Category (forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'seo_name', 'description']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a name...'}),
            'seo_name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a seo_name...'}),
            'description': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a description...'}),
        }
