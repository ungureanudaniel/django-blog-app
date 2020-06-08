from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.db.models import Q
#from django.core.paginator import Paginator, EmptyPage
#from blogproject.config import pagination


#from django.views.generic.list import ListView
#from django.views.generic.detail import DetailView

# Create your views here.
def PostListView(request):
    template_name = 'blogapp/home.html'
    object_list = Post.objects.all()

    context = {
        'object_list': object_list,
    }
    return render(request, template_name, context)

def PostDetailView(request, slug):
    template_name = 'blogapp/post_detail.html'
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post': post,
    }
    return render(request, template_name, context)

def CategoryView(request, slug):
    template_name = 'blogapp/category_detail.html'
    category = get_object_or_404(Category, slug=slug)
    post_categories = Post.objects.filter(category=category)

    context = {
        'category': category,
        'post_categories': post_categories,
    }
    return render(request, template_name, context)

def SearchView(request):
    template_name = 'blogapp/home.html'
    #q is just a word used to store the search word in a dicitonary in the database
    query = request.GET.get('q')
    #this function Q, imported above, returns a search through its arguments: icontains is an "if contains" the word/words before it with double__, then it is stored into our variable results
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))


    context = {
        'query': query,
        'results': results,
    }
    return render(request, template_name, context)
