from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
class database():
    def __init__(self):
        self.myClient = MongoClient("mongodb+srv://quocvi1701:MysV_1701@cluster0.9sp9zvq.mongodb.net/?retryWrites=true&w=majority")
        self.mydb= self.myClient["adventure-game"]
        self.collection_name = self.mydb["statistic"]
        self.is_insert = True
    def get_statistic(self):
        item_details = self.collection_name.find()
        return item_details
        
    def save_statistic(self,name, score, level, mode):
        item_details = self.get_statistic()
        for item in item_details:
            if item["player_name"] == name and item["mode"] == mode:
                self.is_insert = False
                if int(item["score"]) < score:
                    print("check")
                    self.collection_name.update_one({"_id": item["_id"]}, {"$set" : {"score" : score}}) 
                if int(item["level"]) < level:
                    self.collection_name.update_one({"_id": item["_id"]}, {"$set" : {"level" : level}}) 
        if self.is_insert == True:         
            self.collection_name.insert_one({
            "player_name":name,
            "score":score,
            "level":level,
            "mode":mode
            })
    def get_ranking(self, mode):
        pipeline = [
            {"$match": {"mode": mode}},
            {"$sort": {"score": -1}},
        ]
        ranking = self.collection_name.aggregate(pipeline)
        return list(ranking)
