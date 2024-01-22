import pymongo
from pymongo import MongoClient
from typing import Union
from documents import User, Event, EventRequirement, UserRequest

class MongoConnection:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["ticket-tortoise"]

    def has_user(self, discord_id: int) -> bool:
        return self.db.users.find_one({"discord_id": discord_id}) is not None

    def get_user(self, discord_id: int) -> Union[User, None]:
        user_dict = self.db.users.find_one({"discord_id": discord_id})
        if user_dict is None: return None
        else: return User(**user_dict)

    def register_user(self, discord_id: int, name: str) -> bool:
        if self.has_user(discord_id): return False
        user_dict = User(discord_id=discord_id, name=name).to_dict()
        self.db.users.insert_one(user_dict)
        return True

    def has_user_request(self, request_link: str) -> bool:
        return self.db.user_requests.find_one({"request_link": request_link}) is not None

    def create_user_request(self, user_id: int, request_link: str) -> bool:
        if request_link.endswith("/"): request_link = request_link[:-1]
        if self.has_user_request(request_link): return False
        request_dict = UserRequest(user_id=user_id, request_link=request_link).to_dict()
        self.db.user_requests.insert_one(request_dict)
        return True

