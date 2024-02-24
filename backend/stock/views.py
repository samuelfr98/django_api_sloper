from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StockSerializer
from .models import Stock
from django.http import HttpResponse, HttpRequest, JsonResponse
from .etl.gathering_stock_data import YFinanceResponse
import json

# Create your views here.


class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


def index(self):
    return JsonResponse({"Backend response": "200 OK"})


def getTickerNews(request):
    ticker = request.GET.get("ticker")

    gathered_ticker_news = YFinanceResponse.get_ticker_news(
        ticker)
    return JsonResponse(gathered_ticker_news, safe=False)


def getQuote(request):
    ticker = request.GET.get("ticker")

    quote = YFinanceResponse.get_quote(
        ticker)
    return JsonResponse(quote, safe=False)


def getTicker(request):
    ticker = request.GET.get("ticker")

    res = YFinanceResponse.get_ticker(
        ticker)
    return JsonResponse(res, safe=False)


def getChartResponse(request):
    ticker = request.GET.get("ticker")
    period = request.GET.get("period")
    interval = request.GET.get("interval")

    chart_response = YFinanceResponse.get_chart_response(
        ticker=ticker, period=period, interval=interval)
    return JsonResponse(chart_response, safe=False)

def getTechnicalAnalysisIndicators(request):
    ticker = request.GET.get("ticker")
    ta_response = YFinanceResponse.get_technical_analysis_indicators(ticker=ticker)
    return JsonResponse(ta_response, safe=False)