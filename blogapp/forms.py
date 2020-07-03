from django import forms
from .models import Category, Post, About

choices = Category.objects.all().values_list('name', 'name')

choices_list = []

for item in choices::
    choice_list.append(item)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'text', 'image', 'category', 'comment_count', 'created_date', 'status']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title...'}),
            'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title tag...'}),
            'author': forms.TextInput(attrs = {'class': 'form-control', 'value': '', 'id':'ioana', 'type':'hidden'}),
            'category': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            'text' : forms.Textarea(attrs = {'class': 'form-control'}),
            'status': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            #'published_date': forms.DateField(attrs = {'class': 'form-control'}),
            #'created_date': forms.DateField(attrs = {'class': 'form-control'}),
        }

class Category (forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a name...'}),
        }
