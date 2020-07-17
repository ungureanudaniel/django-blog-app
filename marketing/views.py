from django.shortcuts import render


# Create your views here.
#subscription to newsletter
def SubscribeView(request):
    template_name = 'registration/login_2.html'
    model = Subscribe

    if request.method == "POST":
        email =  request.POST["email"]
        new_signup =  Subscribe()
        new_signup.email = email
        new_signup.save()

    return render(request, template_name)