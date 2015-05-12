from pymongo import MongoClient

client=MongoClient()

db=client.test


cursor=db.user.find({"username":"swift"})

l=[]

for c in cursor:
    l.append(c)

s=l[0]

s=str(s)

print s.encode('utf-8')
