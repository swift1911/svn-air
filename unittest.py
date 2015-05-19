from pymongo import MongoClient
import time

client=MongoClient()
db=client.test

print time.ctime()