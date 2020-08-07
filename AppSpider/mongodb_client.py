import pymongo

class Mongo():
    def __init__(self,client,db,col):
        self.myclient = pymongo.MongoClient(client)
        self.mydb = self.myclient[db]
        self.mycol = self.mydb[col]

    def insert_one(self,dict):
        return self.mycol.insert_one(dict).inserted_id



