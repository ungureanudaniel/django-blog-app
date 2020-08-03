from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import About
from .models import Post
from .models import Category
from .forms import CategoryForm, PostForm, CommentForm
#from authentication .forms import UserLoginForm
from .utils import insta_followers_count, fb_followers_count
from authentication.models import Subscribe
from authentication.forms import SubscribeForm
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, get_user_model, login, logout




#from django.views.generic.list import ListView
#from django.views.generic.detail import DetailView



# Create your views here.


def get_category_count():
    queryset = Post.objects.values_list('category').annotate(Count('category'))
    count = queryset.values('category', 'category__count')
    return count

def SubscribeView(request):
    form_class = SubscribeForm
    subscribe_form = form_class(request.POST or None)
    template = "registration/subscribe.html"
    if request.method == "POST":
        if subscribe_form.is_valid():
            instance = subscribe_form.save(commit=False)
            if Subscribe.objects.filter(email=instance.email).exists():
                messages.warning(request, 'Sorry, your email already exists!', "alert alert-warning alert-dismissible")
            else:
                instance.save()
                messages.success(request, 'Your email has been saved', "alert alert-success alert-dismissible")
    context = {
        'subscribe_form': subscribe_form,
    }

    return render(request, template, context)


def UnsubscribeView(request):
    unsubscribe_form = SubscribeForm(request.POST or None)
    template = "registration/unsubscribe.html"
    if unsubscribe_form.is_valid():
        instance = unsubscribe_form.save(commit=False)
        if Subscribe.objects.filter(email=instance.email).exists():
            Subscribe.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been removed', "alert alert-success alert-dismissible")
        else:
            messages.success(request, 'Sorry, but this email does not exist!', "alert alert-warning alert-dismissible")
    context = {
        'unsubscribe_form': unsubscribe_form,
    }

    return render(request, template, context)
#get category for dropdown list
# def get_context_data(self, *args, **kwargs):
#     cat_menu = Category.objects.all()
#     context = super(PostListView, self).get_context_data(self, *args, **kwargs)
#     context["cat_menu"] = cat_menu
#     return context
# nr of views

#add new post
def AddPostView(request):
    template_name = 'blogapp/add_post.html'
    title = 'Create'
    form = PostForm(request.POST, request.FILES or None)
    #categories = Post.objects.all()
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = PostForm()

    context = {
        'title': title,
        'form': form,
    }
    return render(request, template_name, context)


def PostListView(request):
    cat_menu = Category.objects.all()
    print(cat_menu)
    category_count = get_category_count()
    print(category_count)
    template_name = 'blogapp/home.html'
    object_list = Post.objects.filter(status='Published').order_by('-created_date')
    categories = Category.objects.all()
    featured_posts = Post.objects.filter(featured=True, status='Published')
    four_latest = Post.objects.order_by('-created_date')[1:4]
    about_list = About.objects.all()[:1]
    instagram_followers = insta_followers_count()
    fb_followers = fb_followers_count()
    #pagination
    paginator = Paginator(object_list, 3) # Show 2 contacts per page.
    page_request_var = 'page'
    page = request.GET.get('page')
    try:
        page_queryset = paginator.page(page)
    except PageNotAnInteger:
        page_queryset = paginator.page(1)
    except EmptyPage:
        page_queryset = paginator.page(paginator.num_pages)


    context = {
        'cat_menu': cat_menu,
        'categories': categories,
        'category_count': category_count,
        'queryset': page_queryset,
        'page_request_var': page_request_var,
        'featured_posts': featured_posts,
        'fb_followers': fb_followers,
        'about_list': about_list,
        'four_latest': four_latest,
        'object_list': object_list,
        'instagram_followers': instagram_followers,
        #'page_request_var': page_request_var,
    }
    return render(request, template_name, context)

def DraftListView(request):
    template = 'blogapp/draft_posts.html'
    drafts = Post.objects.filter(status='Draft').order_by('created_date')
    about_list = About.objects.all()[:1]
    categories = Category.objects.all()
    category_count = get_category_count()
    featured_posts = Post.objects.filter(featured=True)
    context = {
        'featured_posts': featured_posts,
        'category_count': category_count,
        'categories': categories,
        'about_list': about_list,
        'drafts': drafts,
    }
    return render(request, template, context)


def PostDetailView(request, pk):
    template_name = 'blogapp/post_detail.html'
    about_list = About.objects.all()[:1]
    cat_menu = Category.objects.all()
    #count nr of comments
    nr_comments = Post.objects.values('comments').annotate(Count('comments'))
    count = nr_comments.values('comments', 'comments__count')
    #end nr of comments
    print(nr_comments)
    #model = Post
    post = get_object_or_404(Post, pk=pk)
    posts = Post.objects.filter(pk=pk)
    form = CommentForm(request.POST or None)
    blog_object = Post.objects.get(pk=post.pk)
    blog_object.views_count = blog_object.views_count + 1
    blog_object.save()
    if request.method == "POST":
        if form.is_valid():
            form.instance.post = post
            form.save()
            #return redirect('post', kwargs={'pk':post.pk})
            return redirect(reverse('home'))

    context = {
        'cat_menu': cat_menu,
        'count': count,
        'about_list': about_list,
        'posts': posts,
        'form': form,
    }
    return render(request, template_name, context)

#edit/update a post
def PostEditView(request, pk):
    template_name = 'blogapp/edit_post.html'
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    # categories = Post.objects.all()
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail/edit', pk=post.pk)
        else:
            form = PostForm(instance=post)

    context = {
        'form': form,
    }
    return render(request, template_name, context)

#delete a post
class PostDeleteView(DeleteView):
    template_name = 'blogapp/delete_post.html'
    model = Post
    success_url = reverse_lazy('home')

#category view
def CategoryView(request, cats):
    template_name = 'blogapp/category.html'
    post_categories = Post.objects.filter(category=cats.replace('-', ' '))
    print(post_categories)
    cat_menu = Category.objects.all()
    instagram_followers = insta_followers_count()
    fb_followers = fb_followers_count()
    context = {
        'instagram_followers': instagram_followers,
        'fb_followers': fb_followers,
        'cats': cats.title().replace('-', ' '),
        'cat_menu': cat_menu,
     #   'category': category,
        'post_categories': post_categories,
    }
    return render(request, template_name, context)

#add category
def AddCategoryView(request):
    template_name = 'blogapp/add_category.html'
    form = CategoryForm(request.POST or None)
    #categories = Post.objects.all()
    if request.method == "POST":
        if form.is_valid():
            # name = request.POST.get('name')
            # img = request.POST.get('image')
            messages.success(request, 'Category saved!', "alert alert-success alert-dismissible")
            print('cat_saved')
            form.save()
            return redirect('/')
        else:
            raise Http404
            #form = CategoryForm()
            messages.warning(request, 'Please fill all the fields!', "alert alert-warning alert-dismissible")
    context = {
        'form': form,
    }
    return render(request, template_name, context)


# ABOUT ME VIEW
def AboutView(request):
    template_name = 'blogapp/about.html'
    about_list = About.objects.all()
    instagram_followers = insta_followers_count()
    fb_followers = fb_followers_count()

    context = {
        'fb_followers': fb_followers,
        'instagram_followers': instagram_followers,
        'about_list': about_list,
    }
    return render(request, template_name, context)

# CONTACT VIEW
def ContactView(request):
    template_name = 'blogapp/contact.html'

    if request.method == "POST":
        message_name = request.POST.get('message-name')
        message_email = request.POST.get('message-email')
        message = request.POST.get('message')

        #send email
        if message and message_name and message_email:
            try:
                send_mail(
                message_name,
                message,
                message_email,
                ['ioanad.ungureanu@gmail.com']
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

        render(request, template_name, {'message_name': message_name})
    else:
        return render(request, template_name, {})

def search(request):
    template_name = 'blogapp/search.html'
    about_list = About.objects.all
    category_count = get_category_count()
    featured_posts = Post.objects.filter(featured=True)
    # q is just a word used to store the search word in a dicitonary in the database
    query = request.GET.get('q')

    queryset = Post.objects.all()

    #this function Q, imported above, returns a search through its arguments: icontains is an "if contains" the word/words before it with double__, then it is stored into our variable results
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query)).distinct()

    #pages = pagination(request, results, num=1)

    context = {
        'featured_posts': featured_posts,
        'category_count': category_count,
        'about_list': about_list,
        'queryset': queryset,
    }
    return render(request, template_name, context)
