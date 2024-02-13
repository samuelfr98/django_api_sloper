from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StockSerializer
from .models import Stock
from django.http import HttpResponse, HttpRequest, JsonResponse
from .etl.gathering_stock_data import YFinanceResponse, direct_fetch_from_yfinance_historic, gather_stock_data_no_cache, gather_stock_indicators_over_period, gather_stock_quote, gather_stock_technical_indicators, test, gather_stock_data, check_if_stock_exists_in_db
import json

# Create your views here.


class StockView(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


def index(self):
    return JsonResponse({"Backend response": "200 OK"})


def request(request):
    output = request.GET.get("input")
    return JsonResponse({"output": test(output)})


def gatherStockData(request):
    stock_symbol = request.GET.get("stockSymbol")
    gathered_stock_data = gather_stock_data(stock_symbol)
    return JsonResponse(gathered_stock_data, safe=False)


def gatherStockTechnicalIndicators(request):
    stock_symbol = request.GET.get("stockSymbol")
    gathered_stock_technical_indicators = gather_stock_technical_indicators(
        stock_symbol)
    return JsonResponse(gathered_stock_technical_indicators, safe=False)


def gatherStockQuote(request):
    stock_symbol = request.GET.get("stockSymbol")
    gathered_stock_technical_indicators = gather_stock_quote(
        stock_symbol)
    return JsonResponse(gathered_stock_technical_indicators, safe=False)


def directFetchFromYFinanceHistoric(request):
    stock_symbol = request.GET.get("stockSymbol")
    gathered_stock_technical_indicators = direct_fetch_from_yfinance_historic(
        stock_symbol)
    return JsonResponse(gathered_stock_technical_indicators, safe=False)


def gatherStockIndicatorsOverPeriod(request):
    stock_symbol = request.GET.get("stockSymbol")
    period = request.GET.get("period")
    gathered_stock_technical_indicators = gather_stock_indicators_over_period(
        stock_symbol, period)
    return JsonResponse(gathered_stock_technical_indicators, safe=False)


def gatherStockDataNoCache(request):
    stock_symbol = request.GET.get("stockSymbol")
    start_date = request.GET.get("startDate")
    end_date = request.GET.get("endDate")
    gathered_stock_technical_indicators = gather_stock_data_no_cache(
        stock_symbol, start_date, end_date)
    return JsonResponse(gathered_stock_technical_indicators, safe=False)


def gatherAllTickerInfo(request):
    tickers = request.GET.get("tickers")
    gathered_ticker_info = YFinanceResponse.gather_all_ticker_info(
        tickers)
    return JsonResponse(gathered_ticker_info, safe=False)


def gatherTickerHistory(request):
    ticker = request.GET.get("ticker")
    period = request.GET.get("period")
    interval = request.GET.get("interval")
    gathered_ticker_history = YFinanceResponse.gather_ticker_history(
        ticker, period, interval)
    return JsonResponse(gathered_ticker_history, safe=False)


def gatherTickerHistoryMetadata(request):
    ticker = request.GET.get("ticker")
    period = request.GET.get("period")
    interval = request.GET.get("interval")
    gathered_ticker_history_metadata = YFinanceResponse.gather_ticker_history_metadata(
        ticker, period, interval)
    return JsonResponse(gathered_ticker_history_metadata, safe=False)


def gatherTickerHistoryIncludeAdjustedClose(request):
    ticker = request.GET.get("ticker")
    startDate = request.GET.get("startDate")
    endDate = request.GET.get("endDate")
    gathered_ticker_history_include_adjusted_close = YFinanceResponse.gather_ticker_history_include_adjusted_close(
        ticker, startDate, endDate)
    return JsonResponse(gathered_ticker_history_include_adjusted_close, safe=False)


def gatherTickerNews(request):
    ticker = request.GET.get("ticker")

    gathered_ticker_news = YFinanceResponse.gather_ticker_news(
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
    return JsonResponse(chart_response,safe=False)
