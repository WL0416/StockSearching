from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock
import requests, json

API_KEY = 'OjdiNTAxYWIxMmNmZjAxZDI3YTIwNGQ4Zjc3YTBhZjIy'
URL_TEMP = 'https://api.intrinio.com/prices?identifier=%s&start_date=%s&end_date%s&api_key=%s'
STOCK_CODES = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'INTC', 'CSCO', 'CMCSA', 'PEP', 'NFLX', 'NVDA']

# Create your views here.
def index(request):
    return render(request, 'index.html', {'stock_codes': STOCK_CODES})

def result(request):
    
    if request.method == 'POST':
        
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        stock_code = request.POST.get('code')

        request_url = URL_TEMP % (stock_code, start_date, end_date, API_KEY) 
        
        response = requests.get(request_url)
        
        response = response.json()

        data = response['data']

        if len(data) is not 0:
            stocks = Stock.objects.filter(code=stock_code)
            if(len(stocks)==0):
                for each in data:
                    write2db(stock_code, each)
            else:
                for each in data:
                    stock_in_db = False
                    for stock in stocks:
                        if each['date'] == str(stock.date):
                            stock_in_db = True
                            break
                    if not stock_in_db:
                        write2db(stock_code, each)

        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

# function write new stock record to db
def write2db(code, stock):
    new_stock = Stock(
        code = code,
        date = stock['date'],
        open_price = stock['open'],
        high_price = stock['high'],
        low_price = stock['low'],
        close_price = stock['close'],
        volume = stock['volume']
    )
    new_stock.save()