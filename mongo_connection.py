import pymongo
from pymongo import MongoClient
from typing import Union
from documents import User, Event, EventRequirement

class MongoConnection:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["ticket-tortoise"]
    
    def get_user(self, discord_id: int) -> Union[User, None]:
        user_dict = self.db.users.find_one({"discord_id": discord_id})
        if user_dict is None: return None
        else: return User(**user_dict)
    
    def register_user(self, discord_id: int, name: str):
        user_dict = User(discord_id=discord_id, name=name).to_dict()
        self.db.users.insert_one(user_dict)

