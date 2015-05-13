from pymongo import MongoClient
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