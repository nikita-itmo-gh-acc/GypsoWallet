import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, JsonResponse
from exchange.models import Profile
from django.contrib.auth.models import User
from exchange.forms import *
from django.views.generic import View, ListView, CreateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


class Home(View):
    template_name = "exchange/mainmenu.html"

    def get(self, request, *args, **kwargs):
        u = None
        if request.user.is_authenticated:
            u = request.user
        return render(request, self.template_name, {"user": u})


class Registration(CreateView):
    form_class = RegisterForm
    template_name = 'exchange/register.html'
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'exchange/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context

    def get_success_url(self):
        return reverse_lazy("home")


def logout_view(request):
    logout(request)
    return redirect("home", permanent=True)


def page_not_found(request, exception):
    return HttpResponseNotFound("page not found")


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

    def get(self, request):
        form = self.form_class(initial={"description": request.user.profile.description, })
        return render(request, self.template_name, {"form": form, "user": request.user})


coins = ["bitcoin", "ethereum", "ripple", "litecoin", "binancecoin"]
colors = {"bitcoin": "#8e5ea2",
          "ethereum": "#3e95cd",
          "ripple": "#3cba9f",
          "litecoin": "#e8c3b9",
          "binancecoin": "#c45850"}


@method_decorator(login_required, name='dispatch')
class Crypto(View):
    template_name = 'exchange/crypto.html'
    global coins

    def get(self, request):
        return render(request, self.template_name, {"user": request.user, "crypto_data": coins})


def charts_data(request, coin, days):
    global coins
    url_base = 'https://api.coingecko.com/api/v3/coins/'
    parameters = {
        'vs_currency': "usd",
        'days': days,
        'interval': "daily",
    }
    sess = requests.Session()
    try:
        response = sess.get(url_base + f"{coin}/market_chart", params=parameters)
        if response.status_code == 429:
            return JsonResponse(request.session.get(f"{coin}_last_json"))
        coin_info = json.loads(response.text)
        print(coin_info)
        json_response = {
            "title": f"coins price info for {days} days",
            "data": {
                "labels": list(range(days + 1)),
                "datasets": [{
                    "label": coin,
                    "borderColor": colors[coin],
                    "data": [pair[1] for pair in coin_info["prices"]]
                }]
            }
        }
        request.session[f"{coin}_last_json"] = json_response
        return JsonResponse(json_response)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return HttpResponse(e)


def charts_options(request):
    global coins
    return JsonResponse({
        "options": list(range(7, 31)),
        "coins": coins
    })
