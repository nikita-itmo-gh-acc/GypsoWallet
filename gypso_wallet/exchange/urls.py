from django.urls import path, include

from exchange.views import *

urlpatterns = [
    path('/crypto/<slug:name>/', get_price, name='name'),
    path('', index)
]
