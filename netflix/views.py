from importlib import invalidate_caches
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm
from .forms import LoginForm


def index_view(request):
    """Home page view."""
    return render(request, 'netflix/index.html')

def register_view(request):
    """Registration view."""
    if request.method == 'GET':
        # executed to render the registration page
        register_form = RegisterForm()
        return render(request, 'netflix/register.html', locals())
    else:
        # executed on registration form submission
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            User.objects.create(
                first_name=request.POST.get('firstname'),
                last_name=request.POST.get('lastname'),
                email=request.POST.get('email'),
                username=request.POST.get('email'),
                password=make_password(request.POST.get('password'))
            )
            return HttpResponseRedirect('/login')
        return render(request, 'netflix/register.html', locals())


def login_view(request):
    """Login view."""
    if request.method == 'GET':
        # executed to render the login page
        login_form = LoginForm()
        return render(request, 'netflix/login.html', locals())
    else:
        # get user credentials input
        username = request.POST['email']
        password = request.POST['password']
        # If the email provided by user exists and match the
        # password he provided, then we authenticate him.
        user = authenticate(username=username, password=password)
        if user is not None:
            # if the credentials are good, we login the user
            login(request, user)
            # then we redirect him to home page
            return HttpResponseRedirect('/')
        # if the credentials are wrong, we redirect him to login and let him know
        return render(
            request,
            'netflix/login.html',
            {
                'wrong_credentials': True,
                'login_form': LoginForm(request.POST)
            }
        )

def logout_view(request):
    """Logout view."""
    # logout the request
    logout(request)
    # redirect user to home page
    return HttpResponseRedirect('/')

def checkout(request):
    context = {}
    if request.user:
        if request.method == 'POST':
            message = "From "+request.user.email+"\n"
            message += "Sender name "+request.user.first_name +""+ request.user.last_name+"\n"
            message += "Netflix Payment Done"+"\n"
            try:
                send_mail(
                    'SITE Inquiry'+message,
                    message,
                    request.user.email,
                    ['mane_csit2075@lict.edu.np'],
                    )
                context = {'mail_respone':True }
            except Exception as err:
                raise err
        return render(request,'netflix/checkout.html')

def success_payment(request):
    return render(request,'netflix/success_payment.html',context)


#def success_payment(request):
    if request.method == "POST":
        email = request.POST['username']
        return HttpResponse('')