from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



#from django.views.generic.list import ListView
#from django.views.generic.detail import DetailView

# Create your views here.
def PostListView(request):
    template_name = 'blogapp/home.html'
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 1) # Show 25 contacts per page.
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #if page is not integer, deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'page_request_var': page_request_var,
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

def search(request):
    template_name = 'blogapp/home.html'
    #q is just a word used to store the search word in a dicitonary in the database
    query = request.GET.get('q')
    #this function Q, imported above, returns a search through its arguments: icontains is an "if contains" the word/words before it with double__, then it is stored into our variable results
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    pages = pagination(request, results, num=1)

    context = {
        'items': pages[0],
        'page_range': pages[1],
    }
    return render(request, template_name, context)
