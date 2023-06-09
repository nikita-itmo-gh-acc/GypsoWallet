from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from requests import Session
import json

coins = [{'name': 'bitcoin', }]

# Create your views here.
def index(request):
    return render(request, 'exchange/mainmenu.html')

def get_price(request, name):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'slug':'name',
        'convert':'USDT'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b31509b0-f835-4a30-8dbd-2199c6767dec',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        id = list(data['data'].keys())[0]
        return HttpResponse(data['data'][f'{id}']['quote']['USDT']['price'])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return HttpResponse(e)