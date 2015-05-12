#coding='utf-8
from pymongo import MongoClient
import json


client=MongoClient()

db=client.test


cursor=db.user.find({"username":"swift"})

l=[]

for c in cursor:
    l.append(c)

res=str(l[0]).replace("u'", '').replace("'",'').replace('{', '').replace('}','')

listres=[]

listres=res.split(',')

s=[[0]*2]*len(listres)

i=0

print listres
#decodejson=json.loads(l[0])
