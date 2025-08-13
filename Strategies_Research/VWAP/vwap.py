import yfinance as yf
import pandas as pd
import statistics
import math
import numpy as np
import time 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


#For now input will work but need to automate the input so it can iterate the calculation over a basket of stocks
#Make variables travel between functions so we can seperate functions by task
'''def vwapCalculation():
    #dataDownload; seperate function in future
    endDate = datetime.today()
    startDate = endDate - timedelta(days=10)
    tickerInput = input("Enter a ticker for the stock you want to calculate VWAP for: ")
    ticker=yf.Ticker(tickerInput)
    history = ticker.history(start=startDate, end=endDate) 
    print("History from:\n", history)
    
    #begin calc; seperate function in future
    history['AveragePriceOverT'] = (history['High'] + history['Low'] + history['Close']) / 3
    history['AvgPricexVolume'] = history['AveragePriceOverT'] * history['Volume']
    history['CumAvgPricexVolume'] = history['AvgPricexVolume'].cumsum()
    history['CumVolume'] = history['Volume'].cumsum()
    history['VWAP'] = history['CumAvgPricexVolume'] / history['CumVolume']
    print(history['VWAP'])
'''    



# Uses yFinance library
def getVWAPSpecificData(ticker, days):
    endDate = datetime.today()
    startDate = endDate - timedelta(days=days)
    data=yf.Ticker(ticker)
    history = data.history(start=startDate, end=endDate) #automate dates at some point
    return history

# Reduced memory requirements by not storing every calculation in its own column
def computeVWAP(history):
    
    typical_price = (history['High'] + history['Low'] + history['Close']) / 3
    vwapColumn = (typical_price * history['Volume']).cumsum() / history['Volume'].cumsum()

    return vwapColumn


def vwapCheck(current, vwap):
    if current < vwap:
        print("Send a short order")
    elif current > vwap:
        print("Send a long order")
    else:
        print("Do not send an order")
    return 




#vwapCalculation()




