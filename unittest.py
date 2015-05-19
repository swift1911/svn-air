from pymongo import MongoClient
client=MongoClient()
db=client.test

#db.log.insert_one({"projname":"1","info":[]})

cursor=db.log.find({"projname":"1"})
print cursor.count()