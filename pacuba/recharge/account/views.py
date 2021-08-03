from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.


def register(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "user_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect("send_confirm")
        else:
            form = RegistrationForm()
        return render(request, "register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user_model = get_user_model()
        user = user_model.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, user_model.DoseNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect("index")
    else:
        return redirect("invalid_link")


def logout_view(request):
    logout(request)
    return redirect("index")


def login_view(request, *args, **kwargs):

    user = request.user
    if user.is_authenticated:
        return redirect("index")

    destination = get_redirect_if_exists(request)

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("index")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def forgot(request):
    context = {}
    return render(request, "forgot.html", context)


def send_confirm(request):
    context = {}
    return render(request, 'send_confirm.html', context)

def invalid_link(request):
    context = {}
    return render(request, 'invalid_link.html', context)


def terms(request):
    context = {}
    return render(request, "terms.html", context)


def reset(request):
    context = {}
    return render(request, "reset.html", context)
