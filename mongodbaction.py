from pymongo import MongoClient
import time
class mongodbaction():
    __db=''
    def __init__(self):
        client=MongoClient()
        self.__db=client.test
    
    def authtogetmailaddress(self,group):
        cursor=self.__db.user.find({'usergroup':group})   
        if cursor!=None:
            return cursor
        else:
            return None
    def authtogetusergroup(self,username,pwd):
        cursor=self.__db.user.find_one({'username':username,"userpwd":pwd})   
        if cursor!=None:
            return cursor.get('usergroup')
        else:
            return None
    def insertlog(self,projname,username,action,tagname):
        cursor=self.__db.log.find({"projname":projname})
        if cursor.count()==0:
            self.__db.log.insert_one({"projname":projname,"info":[]})
        self.__db.log.update({"projname":projname},{"$push":{"info":{"username":username,"action":tagname+' '+action,"time":time.ctime()}}})
    