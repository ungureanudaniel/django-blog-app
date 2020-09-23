from django import forms
from .models import Post, About, Comment, Category

choices = Category.objects.all().values_list('name', 'name')

choices_list = []

for item in choices:
    choices_list.append(item)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'author', 'text', 'image', 'category', 'featured', 'status']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title...'}),
            'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title tag...'}),
            'author': forms.Select(attrs = {'class': 'form-control', 'value': '', 'id':'ioana',}),
            'category': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            'text' : forms.Textarea(attrs = {'class': 'form-control'}),
            'status': forms.Select(choices=choices_list, attrs = {'class': 'form-control'}),
            #'featured': forms.Boolean()
            #'published_date': forms.DateField(attrs = {'class': 'form-control'}),
            #'created_date': forms.DateField(attrs = {'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'text']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a name...'}),
            'text' : forms.Textarea(attrs = {'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'image']

        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a name...'}),
        }

class AboutForm(forms.ModelForm):

    class Meta:
        model = About
        fields = ['title', 'text', 'image']

        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a title...'}),
            'text': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Add about yourself...'}),
        }
