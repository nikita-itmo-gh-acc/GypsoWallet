from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from exchange.models import Profile
from django.contrib.auth.models import User
from exchange.forms import *
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required


# Create your views here.
# def index(request):
#     return render(request, "mainmenu.html")


class Home(View):

    def get(self, request, *args, **kwargs):
        return render(request, "exchange/mainmenu.html")


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.data["login"]
            email = form.data["email"]
            password = form.data["password"]
            password_repeat = form.data["password_repeat"]
            if password == password_repeat:
                new_user = User(username=name, email=email, password=password)
                new_user.save()
                new_user.refresh_from_db()
                new_user.profile.description = "test profile is working"
                new_user.save()
                login(request, new_user)
                return redirect("home", permanent=True)
    else:
        form = RegisterForm()
    return render(request, "exchange/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.data["login"]
            password = form.data["password"]
            u = authenticate(username=name, password=password)
            if u is not None:
                login(request, u)
                # p = User.objects.get(email=email)
                # print(p.profile.reg_date)
                return redirect("home", permanent=True)
            else:
                form.add_error("password", "Ошибка авторизации")
                return render(request, "exchange/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "exchange/login.html", {"form": form})


def logout_view(request):
    logout(request)


def page_not_found(request, exception):
    return HttpResponseNotFound("page not found")


@login_required
def profile(request):
    print(request.user.username)
    return render(request, "exchange/profile.html")
