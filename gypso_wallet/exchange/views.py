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
        u = None
        if request.user.is_authenticated:
            u = request.user
        return render(request, "exchange/mainmenu.html", {"user": u})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.data["password"]
            new_user.set_password(password)
            new_user.save()
            # new_user.refresh_from_db()
            # new_user.profile.description = "test profile is working 2"
            # new_user.save()
            login(request, new_user)
            return redirect("home", permanent=True)
    else:
        form = RegisterForm()
    return render(request, "exchange/register.html", {"form": form, "user": None})


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
        return render(request, "exchange/login.html", {"form": form, "user": None})


def logout_view(request):
    logout(request)
    return redirect("home", permanent=True)


def page_not_found(request, exception):
    return HttpResponseNotFound("page not found")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            profile_image, desc = form.cleaned_data["photo"], form.cleaned_data["description"]
            u = request.user
            if profile_image:
                u.profile.photo = profile_image
            u.profile.description = desc
            u.save()
        else:
            form.add_error("description", "Форма некорректна")
    # print(request.user.username)
    else:
        form = ProfileForm(initial={"description": request.user.profile.description,
                                    })
    return render(request, "exchange/profile.html", {"form": form, "user": request.user})
