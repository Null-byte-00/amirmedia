from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from .forms import Profileform
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.


class Signin(View):
    """
    Login view
    """
    def get(self, request):
        return render(request, 'mainapp/signin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/' + user.profile.slug)
        else:
            return render(request, 'mainapp/signin.html', {'error': 'login failed'})


class Signup(View):
    """
    creates User and Profile object from given information and sends
    confirmation email
    """
    def get(self, request):
        form = Profileform()
        return render(request, 'mainapp/signup.html', {'form': form})

    def post(self, request):
        form = Profileform(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.profilepic = form.cleaned_data.get('profilepic')
            user.is_active = False
            user.save()
            user.profile.save()
            html = render_to_string('mainapp/mail/email.html', {
                'user' : user,
                'domain' : get_current_site(request).domain,
                'uidb64' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : account_activation_token.make_token(user),
            })
            mail = EmailMessage('validate your email', html, to=[user.profile.email])
            mail.content_subtype = 'html'
            mail.send()
            return render(request, 'mainapp/mail/email_was_sent.html', {'user': user})
        else:
            return render(request, 'mainapp/signup.html', {'form': form})


# checks confirmation mail
def activate(request, uidb64, token):
    try:
        id = urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk=id)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/signin/')
    else:
        return HttpResponse('email validation failed')


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/signin/')


def home(request):
    return render(request, 'mainapp/home.html')