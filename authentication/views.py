from django.shortcuts import render
from .models import Subscribe
from .forms import SubscribeForm
from django.contrib import messages

# Create your views here.


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
