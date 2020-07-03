from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from .models import Post, Category, About
from marketing.models import Subscribe
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



#from django.views.generic.list import ListView
#from django.views.generic.detail import DetailView

# Create your views here.
def PostListView(request):
    template_name = 'blogapp/home.html'
    object_list = Post.objects.all()
    four_latest = Post.objects.order_by('-created_date')[1:4]
    categories = Category.objects.all()
    about_list = About.objects.all()[:1]

    #paginator = Paginator(object_list, 10) # Show 25 contacts per page.
    #page_request_var = "page"
    #page = request.GET.get(page_request_var)
    #try:
    #    queryset = paginator.page(page)
    #except PageNotAnInteger:
        #if page is not integer, deliver first page
    #    queryset = paginator.page(1)
    #except EmptyPage:
        #if page is out of range, deliver last page
    #    queryset = paginator.page(paginator.num_pages)

    context = {
        'about_list': about_list,
        'categories': categories,
        'four_latest': four_latest,
        'object_list': object_list,
        #'page_request_var': page_request_var,
    }
    return render(request, template_name, context)

def PostDetailView(request, slug):
    template_name = 'blogapp/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    post_categories = Post.objects.filter(category=slug)

    context = {
        'post_categories': post_categories,
        'post': post,
    }
    return render(request, template_name, context)

#subscription to newsletter
def SubscribeView(request):
    template_name = 'blogapp/signin.html'
    model = Subscribe

    if request.method == "POST":
        email =  request.POST["email"]
        new_signup =  Subscribe()
        new_signup.email = email
        new_signup.save()

    return render(request, template_name)


def CategoryView(request, slug):
    template_name = 'blogapp/category_detail.html'
    category = get_object_or_404(Category, slug=slug)
    post_categories = Post.objects.filter(category=category)

    context = {
        'category': category,
        'post_categories': post_categories,
    }
    return render(request, template_name, context)

# ABOUT ME VIEW
def AboutView(request):
    template_name = 'blogapp/about.html'
    about_list = About.objects.all()

    context = {
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
