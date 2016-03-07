from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from pymongo import MongoClient
from tradingDays import getTradeDateInts
import re

def getDay(client, movers_db, collection, date):
    mech = Browser()
    url = "http://online.wsj.com/mdc/public/page/2_3021-losenyse-loser-" + date + ".html?mod=mdc_pastcalendar"
    page = mech.open(url)
    
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table",{"class" : "mdcTable"})
    
    # conditions to remove $ and ,
    rep = {"$": "", ",": ""}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))

    for row in table.findAll("tr", limit=10)[1:]:
        col = row.findAll("td")
        rank = int(col[0].string)
        security = col[1]
        security = security.find("a").string.replace('\n', '').replace('\r', '')
        symbol = security[security.find("(")+1:security.find(")")]
        #price = float(col[2].string.replace('$',''))
        price = pattern.sub(lambda m: rep[re.escape(m.group(0))], col[2].string)
        change_val = float(col[3].string)
        change_percent = float(col[4].string)
        volume = float(col[5].string.replace(',',''))
        post = {"date": date,
                "rank": rank,
                "symbol": symbol, 
                "security": security, 
                "price": price, 
                "change_val": change_val, 
                "change_percent": change_percent, 
                "volume": volume}
        #print post
        post_id = collection.insert_one(post).inserted_id
        post_id

client = MongoClient('localhost', 27017)
movers_db = client.historical_movers
collection = movers_db.winners # names are reversed (winners is actually losers lol)

for date in getTradeDateInts(2015,1,1,2015,10,14):
    print(date)
    getDay(client, movers_db, collection, date)
