from django.shortcuts import render, redirect
import requests
import json
from .models import Stock
from django.contrib import messages
from .forms import StockForm

# Create your views here.


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_key = 'pk_254f9d48d78b49099995618495e71bbd'
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token={}".format(ticker, api_key))
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."

        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock Has Been Added!")
            return redirect('add_stock')
    else:
        output = []
        ticker = Stock.objects.all()
        for item in ticker:
            api_key = 'pk_254f9d48d78b49099995618495e71bbd'
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/{}/quote?token={}".format(str(item), api_key))
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock Has Been Deleted")
    return redirect(add_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})



