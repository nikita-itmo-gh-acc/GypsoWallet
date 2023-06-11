from django.urls import path

from exchange.views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('registration/', Registration.as_view(), name="reg"),
    path('login/', Login.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('logout/', logout_view, name="logout"),
    path('crypto/', Crypto.as_view(), name="crypto"),
    path('charts/<slug:coin>/<int:days>/', charts_data, name="charts"),
    path('charts/options/', charts_options, name="options")
]
