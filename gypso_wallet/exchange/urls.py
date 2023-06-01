from django.urls import path

from exchange.views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('registration/', registration, name="reg"),
    path('login/', login_view, name="login"),
    path('profile/', profile, name="profile"),
    path('logout/', logout_view, name="logout")
]
