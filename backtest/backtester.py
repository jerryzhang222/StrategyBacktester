from get_intraday import get_google_data
from pymongo import MongoClient
from tradingDays import getTradeDateInts
import ystockquote
import pandas as pd
import numpy as np


number_securities = 5
ceiling = 0.015
stop_loss = 0.03
txt_filename = "returns_winners.txt"

client = MongoClient('localhost', 27017)
movers_db = client.historical_movers
collection = movers_db.winners
get_next_day = True
get_tick_data = False
trading_days = getTradeDateInts(2015,1,1,2015,10,14)

def getSecuritiestoBuy(date, number_securities, ceiling, stop_loss, collection, get_next_day, trading_days, returns_txt):
    dictSecurities = {}
    for i in range(1,number_securities+1):
        thisSecurity = str(list(collection.find({'rank': i, 'date': str(date)})))
        symbol = thisSecurity.split("symbol': u'")[1].split("'}")[0]
        price = float(thisSecurity.split("price': u'")[1].split("',")[0])
        dictSecurities[symbol] = price
        print(symbol)
        if get_next_day == True:
            next_date = trading_days[trading_days.index(str(date))+1]
            date_string =  str(next_date)[:4] + "-" + str(next_date)[4:6] + "-" + str(next_date)[6:]
            percent_return = "FUCK"
            try:
                price_data = ystockquote.get_historical_prices(symbol, date_string, date_string)
                next_day_open = float(price_data[date_string]['Open'])
                next_day_close = float(price_data[date_string]['Close'])
                next_day_high = float(price_data[date_string]['High'])
                next_day_low = float(price_data[date_string]['Low'])
                percent_return = (next_day_close - next_day_open)/next_day_open
                low_percent = (next_day_low - next_day_open)/next_day_open
                high_percent = (next_day_high - next_day_open)/next_day_open
            except:
                percent_return = "DEAD_STOCK"
                next_day_open = "DEAD_STOCK"
                next_day_close = "DEAD_STOCK"
                next_day_high = "DEAD_STOCK"
                next_day_low = "DEAD_STOCK"
                low_percent = "DEAD_STOCK"
                high_percent = "DEAD_STOCK"
            returns_txt.write(date_string + "," + symbol + "," + str(percent_return) + "," + str(next_day_high) + "," + str(next_day_low) + "," + str(next_day_open) + "," + str(next_day_close) + "," + str(low_percent) + "," + str(high_percent) + "\n")
    return dictSecurities

def getBacktest(dictSecurities):
    for security, price in dictSecurities.iteritems():
        next_day_prices = get_google_data(security, 180,1) #need to change to actually get the right day
        print next_day_prices
        
returns_txt = open(txt_filename, "w")
returns_txt.write("Date,Ticker,% Return,High,Low,Open,Close,Low %,High %\n")
for date in trading_days:
    print date
    getSecuritiestoBuy(date,5,0,0,collection, get_next_day, trading_days, returns_txt)
returns_txt.close()

#getBacktest(getSecuritiestoBuy(20151001,5,0,0,collection))
#next_day_prices = get_google_data("AAPL", 180,1)
#next_day_prices.to_csv("aapl.csv")
#next_day_prices = pd.read_csv("aapl.csv")
#test = []
#for i in range(1,next_day_prices.shape[0]+1):
#    test.append(["hello", "goodbye"])
#print(pd.concat([next_day_prices, pd.DataFrame(np.matrix(test))], axis=1))


# print(ystockquote.get_historical_prices("AAPL", "2015-10-23", "2015-10-23"))