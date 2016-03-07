from pymongo import MongoClient

client = MongoClient('localhost', 27017)
movers_db = client.historical_movers

#kill today_losers collection
#loser_db.today_losers.drop()
#print(loser_db.collection_names())

#print(movers_db.losers.count())
#find documents
for result_object in movers_db.losers.find({'rank': 1, 'date': '20151002', 'symbol':True}):
#    print("Hello")
    print(result_object)
#    result_object['date']

#find collection size
#print(movers_db.command("dbStats"))
