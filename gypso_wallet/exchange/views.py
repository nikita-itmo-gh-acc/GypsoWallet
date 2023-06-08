from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from exchange.models import Profile
from django.contrib.auth.models import User
from exchange.forms import *
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Home(View):
    template_name = "exchange/mainmenu.html"

    def get(self, request, *args, **kwargs):
        u = None
        if request.user.is_authenticated:
            u = request.user
        return render(request, self.template_name, {"user": u})


class Registration(View):
    form_class = RegisterForm
    template_name = 'exchange/register.html'

    def post(self, request):
        form = self.form_class(request.POST)
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
        form.add_error("password_repeat", "Ошибка регистрации")
        return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "user": None})


class Login(View):
    form_class = LoginForm
    template_name = 'exchange/login.html'

    def post(self, request):
        form = self.form_class(request.POST)
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
                return render(request, self.template_name, {"form": form})

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "user": None})


def logout_view(request):
    logout(request)
    return redirect("home", permanent=True)


def page_not_found(request, exception):
    return HttpResponseNotFound("page not found")


# @method_decorator(login_required, name="post")
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    form_class = ProfileForm
    template_name = 'exchange/profile.html'

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
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
        return render(request, self.template_name, {"form": form, "user": request.user})

    # print(request.user.username)
    def get(self, request):
        form = self.form_class(initial={"description": request.user.profile.description, })
        return render(request, self.template_name, {"form": form, "user": request.user})


@method_decorator(login_required, name='dispatch')
class Crypto(View):
    template_name = 'exchange/crypto.html'

    def get(self, request):
        return render(request, self.template_name, {"user": request.user})
