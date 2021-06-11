from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import datetime
import random
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.utils.html import strip_tags
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from .models import About, Post, Category, Subscriber
from .forms import PostForm, CommentForm, AboutForm, CategoryForm
# from .utils import insta_followers_count, fb_followers_count
# from authentication.models import Subscribe
# from authentication.forms import SubscribeForm
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout


def get_category_count():
    cats = Category.objects.all().annotate(num_posts = Count('postcategory'))
    return cats

#get category for dropdown list
def get_context_data(self, *args, **kwargs):
    cat_menu = Category.objects.all()
    context = super(PostListView, self).get_context_data(self, *args, **kwargs)
    context["cat_menu"] = cat_menu
    return context
# nr of views

#add new post
def AddPostView(request):
    template_name = 'blogapp/add_post.html'
    title = 'Create'
    form = PostForm(request.POST, request.FILES or None)
    categories = Post.objects.all()
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = PostForm()

    context = {
        'categories': categories,
        'title': title,
        'form': form,
    }
    return render(request, template_name, context)


def PostListView(request):
    template_name = 'blogapp/home.html'
    #-------------fetch nr of posts per category------------------------------
    posts_count = get_category_count()

    object_list = Post.objects.filter(status='Published').order_by('-created_date')
    categories = Category.objects.all()
    featured_posts = Post.objects.filter(featured=True, status='Published')
    four_latest = Post.objects.order_by('-created_date')[1:4]
    about_list = About.objects.all()[:1]
    instagram_followers = ""
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
        'posts_count': posts_count,
        'categories': categories,
        'queryset': page_queryset,
        'page_request_var': page_request_var,
        'featured_posts': featured_posts,
        'about_list': about_list,
        'four_latest': four_latest,
        'object_list': object_list,
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

#-------------------------------CATEGORY VIEW-------------------------------------
def PostEditView(request, pk):
    template_name = 'blogapp/edit_post.html'
    post = get_object_or_404(Post, pk=pk)
    #form = PostForm(request.POST or None, request.FILES or None, instance=post)
    categories = Post.objects.all()
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Blog post has been updated')
        except Exception as e:
            messages.warning(request, 'Your post was not saved!')
            #return redirect('post_detail/edit', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'categories': categories,
        'form': form,
        'post': post,
    }
    return render(request, template_name, context)

#delete a post
class PostDeleteView(DeleteView):
    template_name = 'blogapp/delete_post.html'
    model = Post
    success_url = reverse_lazy('home')

#-------------------------------CATEGORY VIEW-------------------------------------
def CategoryView(request, cat_slug):
    template_name = 'blogapp/category.html'
    category = get_object_or_404(Category, slug=cat_slug)
    print(category)
    postsbycategory = Post.objects.filter(category=category)
    print(postsbycategory)
    cat_menu = Category.objects.all()
    context = {
        'cat_menu': cat_menu,
        'category': category,
        'postsbycategory': postsbycategory,
    }
    return render(request, template_name, context)

#-------------------------------ADD CATEGORY VIEW-------------------------------------
def AddCategoryView(request):
    template_name = 'blogapp/add_category.html'
    # form = CategoryForm(request.POST or None)
    categories = Post.objects.all()

    form = CategoryForm(request.POST, request.FILES or None)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = CategoryForm()


    context = {
        'categories': categories,
        'form': form,
    }

    return render(request, template_name, context)


#-------------------------------ADD ABOUT ME VIEW-------------------------------------
def AddAboutView(request):
    template_name = 'blogapp/add_about.html'
    title = 'Create About'
    form = AboutForm(request.POST, request.FILES or None)
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
#-------------------------------ABOUT ME VIEW-------------------------------------
def AboutView(request):
    template_name = 'blogapp/about.html'
    about_list = About.objects.all()
    form = AboutForm(request.POST or None)
    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
        'about_list': about_list,
    }
    return render(request, template_name, context)

#-------------------------------EDIT ABOUT VIEW-------------------------------------
def EditAboutView(request, pk):
    template_name = 'blogapp/edit_about.html'
    about = get_object_or_404(About, pk=pk)
    #form = PostForm(request.POST or None, request.FILES or None, instance=post)
    categories = Post.objects.all()
    if request.method == "POST":
        form = AboutForm(request.POST, instance=about)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Blog post has been updated')
        except Exception as e:
            messages.warning(request, 'Your post was not saved!')
            #return redirect('post_detail/edit', pk=post.pk)
    else:
        form = AboutForm(instance=about)

    context = {
        'form': form,
        'about': about,
    }
    return render(request, template_name, context)


#-------------------------------CONTACT ME VIEW-------------------------------------
def ContactView(request):
    template_name = 'blogapp/contact.html'
    categories = Category.objects.all()
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
                ['danielungureanu531@gmail.com']
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')

        render(request, template_name, {'message_name': message_name, 'categories': categories,})
    else:
        return render(request, template_name, {'categories': categories,})

#-------------------------------SEARCH VIEW-------------------------------------
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

#--------------------------------------LOGIN VIEW-----------------------------------------------
def LoginView(request):
    template = 'registration/login.html'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("login")
    else:
        return render(request, template, {})

#------------------------------------------LOGOUT VIEW-------------------------------------------
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

#-----------------------SEND EMAIL TO SUBSCRIBERS---------------------SEND EMAIL
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

def voucher_code():
    nr_sub = Subscriber.objects.all().count()
    return "Baker{}".format(int(nr_sub)+1)

@csrf_exempt
#--------------------------------------LOGIN VIEW-------------------------------
def SubscribeView(request):
    template = 'blogapp/subscription.html'
    if request.method == "POST":
        sub = Subscriber(email=request.POST.get('sub_email'), name = request.POST.get('sub_name'), voucher_prize = voucher_code(), conf_num=random_digits())
        sub.save()
        sub_subject = "Subscription to Artisan Bakery Brasov"
        from_email=settings.FROM_EMAIL
        sub_message = ''
        html_content='Thank you {} for signing up to my email newsletter! \
                Please complete the process by \
                <a href="{}/subscription_confirmation/?email={}&conf_num={}"> clicking here to \
                confirm your registration</a>.'.format(sub.name, request.build_absolute_uri(''), sub.email, sub.conf_num)
        try:
            send_mail(sub_subject, sub_message, from_email, [sub], html_message=html_content)
            context = {

            }
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, template, {})
#
    else:
        context = {

        }
        return render(request, template, context)
#
# #---------------------------SUBS CONFIRMATION VIEW------------------------------
def subscription_confirmation_view(request):
    template = 'blogapp/subscription_confirmation.html'
    try:
        sub = Subscriber.objects.get(email=request.GET['email'])
        if sub.conf_num == request.GET['conf_num']:
            try:
                sub.confirmed = True
                sub.save()
            except:
                messages.warning(request, "Error! Your email cannot be registered. Please contact us at +40757484560")
            return render(request, template, {'email': sub.email, 'action': 'confirmed'})
        else:
            return render(request, template, {'email': sub.email, 'action': 'denied'})
    except:
        messages.warning(request, "This email already exists in our database!")
        return render(request, template, {})
