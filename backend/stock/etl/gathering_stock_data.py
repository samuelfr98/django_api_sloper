# Importing relevant libraries
from datetime import datetime, timedelta
import json
import math
import re
import sys
from django.http import JsonResponse
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from ..models import PastStockMetric
from django.db.models import Q
from urllib.error import HTTPError


class YFinanceResponse:
    yf.pdr_override()
    
    def gather_all_ticker_info(tickers):   
        # Cleanse extra whitespaces
        tickers_array = tickers.split(' ')
        pattern = re.compile(r'\s+')
        handle_whitespaces = lambda x: re.sub(pattern, '', x)
        stock_symbols_array = list(filter(lambda x: x != '', map(handle_whitespaces, tickers_array)))        
        ticker_count = len(stock_symbols_array)
        tickers = ' '.join(stock_symbols_array)        
        
        output = None
        
        # Fetch multiple tickers at once
        if ticker_count > 1:
            print("Gathering all ticker info for the following input tickers: ", tickers)
            ticker_objects = yf.Tickers(tickers)
            all_results = []
            for stock in stock_symbols_array:
                all_results.append(ticker_objects.tickers[stock].info)
            output = {"results": all_results}
            
        # Fetch one ticker only
        elif ticker_count == 1:
            print("Gathering all ticker info for the following input ticker: ", tickers)
            ticker_object = yf.Ticker(tickers)
            result = ticker_object.info
            output = {"results": result}
            
        # No args
        else:
            output = {"error": f"Malformed input ticker(s). Length of inputs is parsed as {ticker_count}."}
            
        print(output)
        return output
    
    def gather_ticker_history(ticker, period, interval):
        print("Gathering ticker history for the following input ticker: ", ticker)
        
        output = None
        
        if ' ' in ticker:
            output = {"error": "Malformed input ticker(s). Length of inputs is parsed as ${ticker_count}."}
            return output
        
        ticker_info = yf.Ticker(ticker)
        ticker_history = ticker_info.history(period=period, interval=interval, prepost=True)
        ticker_history_json = ticker_history.reset_index().to_dict(orient='records')
        output = {"history": ticker_history_json}
        
        print(output)
        return output

    def gather_ticker_history_metadata(ticker, period, interval):
        print("Gathering ticker history metadata for the following input ticker: ", ticker)
        output = None
        
        if ' ' in ticker:
            output = {"error": "Malformed input ticker(s). Length of inputs is parsed as ${ticker_count}."}
            return output
        
        ticker_info = yf.Ticker(ticker)
        ticker_history = ticker_info.history(period=period, interval=interval, prepost=True)
        ticker_history_metadata = ticker_info.history_metadata
        ticker_history_metadata_json = ticker_history_metadata
        output = {"historyMetaData": ticker_history_metadata_json}
        
        print(output)
        return output
    
    def gather_ticker_history_include_adjusted_close(ticker, startDate=None, endDate=None):
        print("Gathering ticker history including adjusted close for the following input ticker: ", ticker)
        output = None
                
        ticker_object = web.get_data_yahoo(ticker, start=startDate, end=endDate)
        
        print(ticker_object)
        
        ticker_info_json = ticker_object.reset_index().to_dict(orient="records")
        output = {"historyWithAdjustedClose": ticker_info_json}
        
        print(output)
        return output
    
    def gather_ticker_news(ticker):
        print("Gathering ticker news for the following input ticker: ", ticker)
        output = None
        
        ticker_object = yf.Ticker(ticker)
        ticker_news = ticker_object.news
        
        print(ticker_news)
        
        ticker_news_json = ticker_news
        output = {"news": ticker_news_json}
        
        print(output)
        return output
    
    # Specifically for Swift Backend calls. Will likely be cached in this format.
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
            return
        
        quotes = []
                
        for stock in stock_symbols_array:
            ticker_info = ticker_object.tickers[stock].info if ticker_count > 1 else ticker_object.info
            ticker_history = ticker_object.tickers[stock].history if ticker_count > 1 else ticker_object.history
            ticker_history_metadata = ticker_object.tickers[stock].history_metadata if ticker_count > 1 else ticker_object.history_metadata


            # Formatting quote object
            symbol = ticker_info['symbol']
            currency = ticker_info['currency']
            # marketState = ticker_info['']
            fullExchangeName = ticker_info['longName']
            displayName = ticker_info['shortName']
            regularMarketPrice = ticker_info['currentPrice']
            regularMarketPreviousClose = ticker_info['regularMarketPreviousClose']
            regularMarketTime = ticker_history_metadata['regularMarketTime']
            # postMarketPrice = ticker_info['']
            # postMarketChange = ticker_info['']
            regularMarketOpen = ticker_info['regularMarketOpen']
            regularMarketDayHigh = ticker_info['regularMarketDayHigh']
            regularMarketDayLow = ticker_info['regularMarketDayLow']
            regularMarketVolume = ticker_info['regularMarketVolume']
            trailingPE = ticker_info['trailingPE']
            marketCap = ticker_info['marketCap']
            fiftyTwoWeekLow = ticker_info['fiftyTwoWeekLow']
            fiftyTwoWeekHigh = ticker_info['fiftyTwoWeekHigh']
            averageVolume = ticker_info['averageVolume']
            trailingAnnualDividendYield = ticker_info['trailingAnnualDividendYield']
            trailingEps = ticker_info['trailingEps']
            
            regularMarketChange = regularMarketPrice - regularMarketOpen
            regularMarketChangePercent = (regularMarketChange/regularMarketOpen)*100
            regularMarketChangePreviousClose = regularMarketPrice - regularMarketPreviousClose
            
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
                # 'regularMarketTime': regularMarketTime, ## epoch time
                'regularMarketTime': datetime.utcfromtimestamp(regularMarketTime).isoformat(), ## iso time
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
            }

            quotes.append(quote)
        

        output = {"quote": quotes}

        print(output)
    
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
            ticker_history = ticker_object.tickers[stock].history if ticker_count > 1 else ticker_object.history
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
        
        print(ticker_history)

        # Formatting chartMeta fields
        currency = ticker_info['currency']
        symbol = ticker_info['symbol']
        regularMarketPrice = ticker_info['currentPrice']
        previousClose = ticker_info['previousClose']
        gmtOffSetMilliseconds = ticker_info['gmtOffSetMilliseconds']
        regularTradingPeriodStartDate = ticker_history_metadata['currentTradingPeriod']['regular']['start']
        regularTradingPeriodEndDate = ticker_history_metadata['currentTradingPeriod']['regular']['end']
        
        
        # Formatting indicator values
        ticker_history_dict = ticker_history.reset_index().to_dict(orient='records')

        indicator = {
            # public let timestamp: Date
            # public let open: Double
            # public let high: Double
            # public let low: Double
            # public let close
        }

        chartMeta = {
            'currency': currency,
            'symbol': symbol,
            'regularMarketPrice': regularMarketPrice,
            'previousClose': previousClose,
            'gmtOffSetMilliseconds': gmtOffSetMilliseconds,
            # 'regularTradingPeriodStartDate': regularTradingPeriodStartDate, ## epoch
            'regularTradingPeriodStartDate': datetime.utcfromtimestamp(regularTradingPeriodStartDate).isoformat(), ## iso
            # 'regularTradingPeriodEndDate': regularTradingPeriodEndDate,     ## epoch      
            'regularTradingPeriodEndDate': datetime.utcfromtimestamp(regularTradingPeriodEndDate).isoformat(),     ## iso      
        }

        chartResponse = {
            'meta': chartMeta,
            'indicators': ticker_history_dict
        }
        
        output = {"chartResponse": chartResponse}
    
        return output






##### Below functions will be removed in near future. Above class methods are more reliable, well formatted, and useable. 






def test(input):
    print(input)
    return "test call lstm with input: " + input

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

###################        Simplified for Swift GUI         #####################
def gather_stock_data_no_cache(stockSymbol, startDate = None, endDate = None):
    print("Querying yfinance you motherfucking motherfucker!")
    yf.pdr_override()
    today = datetime.today()
    end_date = today.strftime('%Y-%m-%d') if endDate is None else endDate
    start_date = (today - timedelta(weeks=7*52)).strftime('%Y-%m-%d') if startDate is None else startDate
    df = web.get_data_yahoo(
        f'{stockSymbol}', start=f'{start_date}', end=f'{end_date}')
    # Convert df to JSON
    all_dates = df['Close'].keys()
    print(all_dates)
    elements = [
        {
            "date": datetime.date(date),
            "open": float(f"{df['Open'][date]:.2f}"),
            "close": float(f"{df['Close'][date]:.2f}"),
            "high": float(f"{df['High'][date]:.2f}"),
            "low": float(f"{df['Low'][date]:.2f}"),
            "volume": int(df['Volume'][date]),
        }
        for i, date in enumerate(all_dates)
    ]
    new_json = {"stockSymbol": stockSymbol,
                "metrics": elements}
    return new_json

def gather_stock_quote(stockSymbol):
    print("Querying yfinance directly you motherfucking motherfucker (for quote data)!")
    print(stockSymbol)
    yf.pdr_override()
    yf_response = None
    final_output = None
    final_output = {
        "quoteResponse": {
            "result": None,
            "error": None
        }
    }
    try:
        yf_response = yf.Tickers(stockSymbol)
        all_results = []
        stock_symbols_array = stockSymbol.split(' ')
        for stock in stock_symbols_array:
            all_results.append(yf_response.tickers[stock].info)

        final_output["quoteResponse"]["result"] = all_results

    except KeyError as e:
        final_output["quoteResponse"]["error"] = {
            "description": "KeyError. There may be a typo in your stock symbol(s)."}
        print("%s - %s at line: %s" % (sys.exc_info()
              [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
    except:
        final_output["quoteResponse"][
            "error"] = {
            "description": "Unknown Error. There may be a typo in your stock symbol(s)."}
        print("%s - %s at line: %s" % (sys.exc_info()
              [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

    return final_output


def direct_fetch_from_yfinance_historic(stockSymbol):
    print("Querying yfinance you motherfucking motherfucker!")
    yf.pdr_override()
    today = datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - timedelta(weeks=7*52)).strftime('%Y-%m-%d')
    df = web.get_data_yahoo(
        f'{stockSymbol}', start=f'{start_date}', end=f'{end_date}')

    print(df)
    # Convert df to JSON
    json_output = json.loads(df.to_json(orient='records'))

    return json_output


def gather_stock_indicators_over_period(stockSymbol, period = None):
    print("Querying yfinance directly you motherfucking motherfucker!")
    print(stockSymbol)

    time_range = period if period is not None else '1mo' 

    yf.pdr_override()
    yf_response = None
    final_output = None

    final_output = {
            "result": None,
            "error": None
    }

    try:
        yf_response = yf.Tickers(stockSymbol)
        all_results = []
        stock_symbols_array = stockSymbol.split(' ')
        for stock in stock_symbols_array:
            all_results.append(json.loads(yf_response.tickers[stock].history(
                period=time_range, interval="1m").to_json(orient="records")))

        #### JSON IS MALFORMED WITHOUT DATETIMES. CONSIDER FORMATTING WITH EXAMPLE PRINTED BELOW
        print(yf_response.tickers["MSFT"].history(
                period=time_range, interval="1m"))

        final_results = []
        for i, res in enumerate(all_results):
            final_results.append({stock_symbols_array[i]: res})

        final_output["result"] = final_results

    except KeyError as e:
        final_output["error"] = {
            "description": "KeyError. There may be a typo in your stock symbol(s)."}
        print("%s - %s at line: %s" % (sys.exc_info()
              [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
    except:
        final_output[
            "error"] = {
            "description": "Unknown Error. There may be a typo in your stock symbol(s)."}
        print("%s - %s at line: %s" % (sys.exc_info()
              [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))

    return final_output



###     ###     TECHNICAL INDICATORS FUNCTIONS     ###     ###


def gather_stock_technical_indicators(stock_symbol):
    # need_to_fetch = check_if_stock_exists_in_db(input)
    # print("Need to calculate indicators from scratch? ", need_to_fetch)
    # df = None
    # if not need_to_fetch:
    #     df = fetch_from_database(input)
    # else:
    #     df = fetch_from_yfinance(input)
    #     metrics = df["metrics"]
    #     cache_stock_data(metrics, input)

    # print(df["metrics"][0])

    # return df

    return None
