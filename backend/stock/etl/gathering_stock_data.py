# Importing relevant libraries
from datetime import datetime, timedelta
import json
import math
import re
import sys
import time
import dateutil.parser as dp
from django.http import JsonResponse
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from ..models import PastStockMetric
from django.db.models import Q
from urllib.error import HTTPError
import talib
from talib import stream
talib.set_compatibility(1)


class YFinanceResponse:
    yf.pdr_override()
    
    def get_ticker_news(ticker):
        print("Gathering ticker news for the following input ticker: ", ticker)
        output = None
        
        ticker_object = yf.Ticker(ticker)
        ticker_news = ticker_object.news
        
        print(ticker_news)
        
        ticker_news_json = ticker_news
        output = {"news": ticker_news_json}
        
        print(output)
        return output
    
    def get_quote(ticker):
        # Cleanse extra whitespaces
        tickers_array = ticker.split(' ')
        pattern = re.compile(r'\s+')
        handle_whitespaces = lambda x: re.sub(pattern, '', x)
        stock_symbols_array = list(filter(lambda x: x != '', map(handle_whitespaces, tickers_array)))        
        ticker_count = len(stock_symbols_array)
        ticker = ' '.join(stock_symbols_array)        
        
        ticker_object = None
        
        # Fetch multiple tickers at once
        if ticker_count > 1:
            print("Getting quote for the following input tickers: ", ticker)
            ticker_object = yf.Tickers(ticker)

            
        # Fetch one ticker only
        elif ticker_count == 1:
            print("Getting quote for the following input ticker: ", ticker)
            ticker_object = yf.Ticker(ticker)
            
        # No args
        else:
            print("We have no args!")
            return
        
        quotes = []
        
        print("We got the ticker shit")

                
        for stock in stock_symbols_array:
            ticker_info = ticker_object.tickers[stock].info if ticker_count > 1 else ticker_object.info
            ticker_history = ticker_object.tickers[stock].history(interval="1d", period="1d") if ticker_count > 1 else ticker_object.history(interval="1d", period="1d")
            ticker_history_metadata = ticker_object.tickers[stock].history_metadata if ticker_count > 1 else ticker_object.history_metadata            

            # Formatting quote object
            symbol = ticker_info['symbol']  if 'symbol' in ticker_info.keys() else None
            currency = ticker_info['currency']  if 'currency' in ticker_info.keys() else None
            # marketState = ticker_info['']
            fullExchangeName = ticker_info['exchange']  if 'exchange' in ticker_info.keys() else None
            displayName = ticker_info['shortName']  if 'shortName' in ticker_info.keys() else None
            regularMarketPrice = ticker_info['currentPrice']  if 'currentPrice' in ticker_info.keys() else None
            regularMarketPreviousClose = ticker_info['regularMarketPreviousClose']  if 'regularMarketPreviousClose' in ticker_info.keys() else None
            regularMarketTime = ticker_history_metadata['regularMarketTime']  if 'regularMarketTime' in ticker_info.keys() else None
            # postMarketPrice = ticker_info['']
            # postMarketChange = ticker_info['']
            regularMarketOpen = ticker_info['regularMarketOpen']  if 'regularMarketOpen' in ticker_info.keys() else None
            regularMarketDayHigh = ticker_info['regularMarketDayHigh']  if 'regularMarketDayHigh' in ticker_info.keys() else None
            regularMarketDayLow = ticker_info['regularMarketDayLow']  if 'regularMarketDayLow' in ticker_info.keys() else None
            regularMarketVolume = ticker_info['regularMarketVolume']  if 'regularMarketVolume' in ticker_info.keys() else None
            trailingPE = ticker_info['trailingPE']  if 'trailingPE' in ticker_info.keys() else None
            marketCap = ticker_info['marketCap']  if 'marketCap' in ticker_info.keys() else None
            fiftyTwoWeekLow = ticker_info['fiftyTwoWeekLow']  if 'fiftyTwoWeekLow' in ticker_info.keys() else None
            fiftyTwoWeekHigh = ticker_info['fiftyTwoWeekHigh']  if 'fiftyTwoWeekHigh' in ticker_info.keys() else None
            averageVolume = ticker_info['averageVolume']  if 'averageVolume' in ticker_info.keys() else None
            trailingAnnualDividendYield = ticker_info['trailingAnnualDividendYield'] if 'trailingAnnualDividendYield' in ticker_info.keys() else None
            trailingEps = ticker_info['trailingEps']  if 'trailingEps' in ticker_info.keys() else None
            regularMarketChange = regularMarketPrice - regularMarketPreviousClose
            regularMarketChangePercent = (regularMarketChange/regularMarketOpen)*100
            regularMarketChangePreviousClose = regularMarketPrice - regularMarketPreviousClose
            beta = ticker_info['beta']  if 'beta' in ticker_info.keys() else None
            yield_var = ticker_info ['dividendYield']  if 'dividendYield' in ticker_info.keys() else None
            
            quote = {
                'symbol': symbol,
                'currency': currency,
                'fullExchangeName': fullExchangeName,
                'displayName': displayName,
                'regularMarketPrice': regularMarketPrice,
                'regularMarketChange': regularMarketChange,
                'regularMarketChangePercent': regularMarketChangePercent,
                'regularMarketChangePreviousClose': regularMarketChangePreviousClose,
                'regularMarketPreviousClose': regularMarketPreviousClose,
                'regularMarketTime': regularMarketTime, ## epoch time
                # 'regularMarketTime': datetime.utcfromtimestamp(regularMarketTime).isoformat(), ## iso time
                'regularMarketOpen': regularMarketOpen,
                'regularMarketDayHigh': regularMarketDayHigh,
                'regularMarketDayLow': regularMarketDayLow,
                'regularMarketVolume': regularMarketVolume,
                'trailingPE': trailingPE,
                'marketCap': marketCap,
                'fiftyTwoWeekLow': fiftyTwoWeekLow,
                'fiftyTwoWeekHigh': fiftyTwoWeekHigh,
                'averageVolume': averageVolume,
                'trailingAnnualDividendYield': trailingAnnualDividendYield,
                'trailingEps': trailingEps,
                'beta': beta,
                'yield': yield_var
            }

            quotes.append(quote)
        

        output = {"quote": quotes}
    
        return output

    def get_ticker(ticker):        
        # Cleanse extra whitespaces
        tickers_array = ticker.split(' ')
        pattern = re.compile(r'\s+')
        handle_whitespaces = lambda x: re.sub(pattern, '', x)
        stock_symbols_array = list(filter(lambda x: x != '', map(handle_whitespaces, tickers_array)))        
        ticker_count = len(stock_symbols_array)
        ticker = ' '.join(stock_symbols_array)        
        
        ticker_object = None
        
        # Fetch multiple tickers at once
        if ticker_count > 1:
            print("Getting ticker for the following input tickers: ", ticker)
            ticker_object = yf.Tickers(ticker)

            
        # Fetch one ticker only
        elif ticker_count == 1:
            print("Getting ticker for the following input ticker: ", ticker)
            ticker_object = yf.Ticker(ticker)
            
        # No args
        else:
            output = {"error": f"Malformed input ticker(s). Length of inputs is parsed as {ticker_count}."}
        
        tickers = []
                
        for stock in stock_symbols_array:
            ticker_info = ticker_object.tickers[stock].info if ticker_count > 1 else ticker_object.info
            ticker_history = ticker_object.tickers[stock].history(interval="1d", period="1d") if ticker_count > 1 else ticker_object.history(interval="1d", period="1d")
            ticker_history_metadata = ticker_object.tickers[stock].history_metadata if ticker_count > 1 else ticker_object.history_metadata

            # Formatting ticker object
            symbol = ticker_info['symbol']
            quoteType = ticker_info['quoteType']
            shortName = ticker_info['shortName']
            longName = ticker_info['longName']
            sector = ticker_info['sector']
            industry = ticker_info['industry']
            exchangeName = ticker_history_metadata['exchangeName']

            ticker = {
                'symbol': symbol,
                'quoteType': quoteType,
                'shortName': shortName,
                'longName': longName,
                'sector': sector,
                'industry': industry,
                'exchangeName': exchangeName,
            }

            tickers.append(ticker)
        

        output = {"ticker": tickers}
    
        return output

    def get_chart_response(ticker, period, interval):
        yf.pdr_override()
        
        print("Getting chart response for the following input ticker: ", ticker)
        
        ticker_object = yf.Ticker(ticker)
        ticker_history = yf.Ticker(ticker).history(period=period, interval=interval)
        ticker_info = ticker_object.info
        ticker_history_metadata = ticker_object.history_metadata
        
        # Formatting chartMeta fields
        currency = ticker_info['currency']
        symbol = ticker_info['symbol']
        regularMarketPrice = ticker_info['currentPrice']
        previousClose = ticker_info['previousClose']
        gmtOffSetMilliseconds = ticker_info['gmtOffSetMilliseconds']
        regularTradingPeriodStartDate = ticker_history_metadata['currentTradingPeriod']['regular']['start']
        regularTradingPeriodEndDate = ticker_history_metadata['currentTradingPeriod']['regular']['end']

        chartMeta = {
            'currency': currency,
            'symbol': symbol,
            'regularMarketPrice': regularMarketPrice,
            'previousClose': previousClose,
            'gmtOffSetMilliseconds': gmtOffSetMilliseconds,
            'regularTradingPeriodStartDate': regularTradingPeriodStartDate, ## convert to epoch
            # 'regularTradingPeriodStartDate': datetime.utcfromtimestamp(regularTradingPeriodStartDate).isoformat(), ## iso
            'regularTradingPeriodEndDate': regularTradingPeriodEndDate,     ## convert to epoch      
            # 'regularTradingPeriodEndDate': datetime.utcfromtimestamp(regularTradingPeriodEndDate).isoformat(),     ## iso      
        }
                
        # Formatting indicator values
        ticker_history_df = ticker_history.reset_index()
        
        # indicator = {
        #     # public let datetime: Date?
        #     # public let date: Date?
        #     # public let open: Double
        #     # public let high: Double
        #     # public let low: Double
        #     # public let close
        # }
        # Date or Datetime key is used depending on period and interval inputs. Standardize to always output as date key.
        if 'Datetime' in ticker_history_df: 
            ticker_history_df = ticker_history_df.rename(columns={'Datetime': 'Date'})
        
        
        # Convert indicator Date to epoch time
        # "Date":     "2024-02-20T00:00:00-05:00"

        ticker_history_df['Date'] = ticker_history_df['Date'].apply(lambda item: int(item.timestamp()))
        
        ticker_history_dict = ticker_history_df.to_dict(orient='records')

        chartResponse = {
            'meta': chartMeta,
            'indicators': ticker_history_dict
        }
        
        output = {"chartResponse": chartResponse}
        # print(output)
    
        return output

    def get_recommended_strategy(ticker):
        yf.pdr_override()
        
        ticker_object = yf.Ticker(ticker)
        ticker_info = ticker_object.info
        
        # From info
        overallRisk = ticker_info['overallRisk'] if 'overallRisk' in ticker_info.keys() else None
        recommendationKey = ticker_info['recommendationKey'] if 'recommendationKey' in ticker_info.keys() else None
        recommendationMean = ticker_info['recommendationMean'] if 'recommendationMean' in ticker_info.keys() else None
        
        recommendations = {
            'overallRisk': overallRisk,
            'recommendationKey': recommendationKey,
            'recommendationMean': recommendationMean
        }
        
        output = {'recommendations': recommendations}
        
        return output
        
    def get_technical_analysis_indicators(ticker):
        
        print("Getting technical indicators for: ", ticker)
                
        previous_twohundred_days_indicators = pd.DataFrame(YFinanceResponse.get_chart_response(ticker=ticker, period='200d', interval='1d')['chartResponse']['indicators'])
        print(previous_twohundred_days_indicators)

        closes= np.array(previous_twohundred_days_indicators['Close'])
        highs= np.array(previous_twohundred_days_indicators['High'])
        lows= np.array(previous_twohundred_days_indicators['Low'])
        volumes= np.array(previous_twohundred_days_indicators['Volume']).astype(float)
                
        ten_day_sma_close = DeriveTechnicalIndicator.simple_moving_average(arr=closes[190:200])
        fifty_day_sma_close = DeriveTechnicalIndicator.simple_moving_average(arr=closes[150:200])
        twohundred_day_sma_close = DeriveTechnicalIndicator.simple_moving_average(arr=closes)
        ten_day_wma_close = DeriveTechnicalIndicator.weighted_moving_average(arr=closes[190:200])
        ten_day_ema_close = DeriveTechnicalIndicator.exponential_moving_average(arr=closes[190:200])
        rsi = DeriveTechnicalIndicator.relative_strength_index(arr=closes)
        cci = DeriveTechnicalIndicator.commodity_channel_index(
            closes=closes[180:200],
            highs=highs[180:200],
            lows=lows[180:200]
        )
        ad = DeriveTechnicalIndicator.accumulation_distribution(
            highs=highs,
            lows=lows,
            closes=closes,
            volumes=volumes
        )
        print(ad)
        
        slow_sto_k, slow_sto_d = DeriveTechnicalIndicator.slow_stochastic(
            highs=highs,
            lows=lows,
            closes=closes
        )
        macd = DeriveTechnicalIndicator.moving_average_convergence_divergence(closes=closes)
        bbands = DeriveTechnicalIndicator.bolinger_bands(close_arr=closes)
        
        technical_indicators = {
            ticker: {
                'ten_day_sma_close': ten_day_sma_close,
                'fifty_day_sma_close': fifty_day_sma_close,
                'twohundred_day_sma_close': twohundred_day_sma_close,
                'wma_close': ten_day_wma_close,
                'ema_close': ten_day_ema_close,
                'rsi': rsi,
                'cci': cci,
                'ad': ad,
                'sto_k': slow_sto_k,
                'sto_d': slow_sto_d,
                'macd': macd,
                'bbands': bbands
            }
        }
        
        print(technical_indicators)
        return technical_indicators
    

class CacheData:
    def cacheTicker(symbol):
        ticker_from_database = QueryDatabase.queryTicker(symbol)
        if len(ticker_from_database)==0:
            new_ticker = YFinanceResponse.get_ticker(symbol)
            # Add ticker to database

        # return ticker from database
        print("Ticker has been cached!")

    def cacheQuote(symbol):
        quote_from_database = QueryDatabase.queryQuote(symbol)
        if len(quote_from_database)==0:
            new_quote = YFinanceResponse.get_ticker(symbol, int(time.time))
            # Add quote to database

        # return quote from database
        return "Quote has been cached!"

    def cacheChartMeta(symbol):
        chart_meta_from_database = QueryDatabase.queryChartMeta(symbol)
        if len(chart_meta_from_database)==0:
            new_chart_meta = YFinanceResponse.get_ticker(symbol, int(time.time))
            # Add chart_meta to database

        # return chart_meta from database
        return "Chart Meta has been cached!"

    def cacheHistoricIndicator(symbol, date):
        historic_indicator_from_database = QueryDatabase.queryHistoricIndicator(symbol, date)
        if len(historic_indicator_from_database)==0:
            new_historic_indicator = YFinanceResponse.get_historic_indicator(symbol, date)
            # Add historic_indicator to database

        # return historic_indicator from database
        return "Historic Indicator has been cached!"

class QueryDatabase:
    def queryTicker(symbol):
        print("Checking if ticker exists in database you mother fucking bozo!")
        ticker_from_database = PastStockMetric.objects.filter(
            Q(stock_symbol=f'{symbol}')
        ).values()
        return ticker_from_database
    
    def queryQuote(symbol, currentTime):
        # should update at most once per minute per stock
        return "Checking if quote exists in database you mother fucking bozo!"

    def queryChartMeta(symbol, currentTime):
        # should update at most once per day
        return "Checking if ticker exists in database you mother fucking bozo!"

    def queryHistoricIndicator(symbol, date):
        # should update at most once per day
        return "Checking if historic indicator exists in database you mother fucking bozo!"

class DeriveTechnicalIndicator:
    
    def simple_moving_average(arr):
        output = np.average(arr)
        return output
    
    def weighted_moving_average(arr):
        wma = talib.WMA(arr, len(arr))
        output=wma[len(wma)-1]
        return output
    
    def exponential_moving_average(arr):
        ema = talib.EMA(np.array(arr), timeperiod=len(arr))
        output = ema[len(ema)-1]
        return output
    
    def relative_strength_index(arr):
        rsi = talib.RSI(arr, len(arr))
        output = rsi[len(rsi)-1]
        return output
    
    def commodity_channel_index(highs, lows, closes):
        assert(len(highs) == len(lows) == len(closes))
        cci = talib.CCI(high=highs, low=lows, close=closes, timeperiod=len(highs))
        output = cci[len(cci)-1]
        return output
    
    def accumulation_distribution(highs, lows, closes, volumes):
        ad = talib.AD(high=highs, low=lows, close=closes, volume=volumes)
        output = ad[len(ad)-1]
        return output
    
    def fast_stochastic(closes, lows, highs):
        fast_k, fast_d = talib.STOCHF(high=highs, low=lows, close=closes)
        output = {"fast_k": fast_k[len(fast_k)-1], "fast_d": fast_d[len(fast_d)-1]}
        return output
    
    def slow_stochastic(closes, lows, highs):
        slow_k, slow_d = talib.STOCH(high=highs, low=lows, close=closes)
        slow_k = slow_k[len(slow_k)-1]
        slow_d = slow_d[len(slow_d)-1]
        return slow_k, slow_d
    
    def moving_average_convergence_divergence(closes):
        macd, macdsignal, macdhist = talib.MACDFIX(closes)
        output = macd[len(macd)-1]
        print(output)
        return output
    
    def bolinger_bands(close_arr):
        upperband, middleband, lowerband = talib.BBANDS(close_arr)
        return middleband[len(middleband)-1]
    
    
##### Below functions will be removed in near future. Above class methods are more reliable, well formatted, and useable. 

# Collects last 7 years of data from Yahoo Finance API
# Input: string representing stock symbol


def gather_stock_data(input):
    need_to_fetch = check_if_stock_exists_in_db(input)
    print("Need to fetch? ", need_to_fetch)
    df = None
    if not need_to_fetch:
        df = fetch_from_database(input)
    else:
        df = fetch_from_yfinance(input)
        metrics = df["metrics"]
        cache_stock_data(metrics, input)

    print(df["metrics"][0])

    return df


###     ###     HELPER FUNCTIONS     ###     ###

def cache_stock_data(metrics, stock_symbol):
    print("Saving yfinance responses to database, AKA, cacheing that bitch!")

    cache = [
        PastStockMetric(stock_symbol=stock_symbol,
                        date=metric[i]["Date"],
                        full_name=stock_symbol,
                        open_price=metric[i]["Open"],
                        close_price=metric[i]["Close"],
                        high_price=metric[i]["High"],
                        low_price=metric[i]["Low"],
                        volume=metric[i]["Volume"])
        for i, metric in enumerate(metrics)
    ]

    print("attempting bulk create!")
    inserting = PastStockMetric.objects.bulk_create(cache)
    print("Completed bulk create!")


def check_if_stock_exists_in_db(stockSymbol):
    # Only checks if stock symbol exists at all in database. Next steps will include checking if stock symbol exists, then also checking if specific dates exist and adding any new ones.
    # Currently returns boolean. After above improvement, will return all dates that stock exists for.
    print("Checking if stock exists in database. If it does, we'll eat at home; otherwise, we'll eat at yfinance!")
    existing_data = PastStockMetric.objects.filter(
        Q(stock_symbol=f'{stockSymbol}')).values()

    return (len(existing_data) == 0)


def fetch_from_yfinance(stockSymbol):
    print("Querying yfinance you motherfucking motherfucker!")
    yf.pdr_override()
    today = datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - timedelta(weeks=7*52)).strftime('%Y-%m-%d')
    df = web.get_data_yahoo(
        f'{stockSymbol}', start=f'{start_date}', end=f'{end_date}')

    # Convert df to JSON
    json_output = convert_yfinance_df_to_json(df, stockSymbol)

    return json_output


def fetch_from_database(stockSymbol):
    print("No need to query yfinance you motherfucking motherfucker. We have stocks at home :)")
    data = PastStockMetric.objects.filter(
        Q(stock_symbol=f'{stockSymbol}')).values()

    # Convert queryset to JSON
    json_output = convert_db_queryset_to_json(data, stockSymbol)

    return json_output


def convert_yfinance_df_to_json(df, stockSymbol):
    all_dates = df['Close'].keys()
    elements = [
        {
            i: {
                "Date": datetime.date(date),
                "Open": f"{df['Open'][date]:.2f}",
                "Close": f"{df['Close'][date]:.2f}",
                "High": f"{df['High'][date]:.2f}",
                "Low": f"{df['Low'][date]:.2f}",
                "Volume": int(df['Volume'][date]),
            }
        }
        for i, date in enumerate(all_dates)
    ]

    new_json = {"stockSymbol": stockSymbol,
                "metrics": elements}

    return new_json


def convert_db_queryset_to_json(queryset, stockSymbol):

    elements = [
        {
            i: {
                "Date": record['date'],
                "Open": f"{record['open_price']:.2f}",
                "Close": f"{record['close_price']:.2f}",
                "High": f"{record['high_price']:.2f}",
                "Low": f"{record['low_price']:.2f}",
                "Volume": int(record['volume']),
            }
        }
        for i, record in enumerate(queryset)
    ]

    new_json = {"stockSymbol": stockSymbol,
                "metrics": elements}

    return new_json

