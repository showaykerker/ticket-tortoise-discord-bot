import unittest
from mongo_connection import MongoConnection

class TestMongoConnection(unittest.TestCase):
    def setUp(self):
        self.mongo = MongoConnection()
        
    def test_mongo_connection_user_existing(self):
        # Test case for an existing user
        discord_id = 111111111
        name = "John Doe"
        self.mongo.register_user(discord_id, name)
        user = self.mongo.get_user(discord_id)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.create_date)
        self.assertEqual(user.discord_id, discord_id)
        self.assertEqual(user.name, name)
    
    def test_mongo_connection_user_non_existing(self):
        # Test case for a non-existing user
        discord_id = 987654321
        user = self.mongo.get_user(discord_id)
        self.assertIsNone(user)
    
    def tearDown(self):
        self.mongo.db.users.delete_many({})

if __name__ == '__main__':
    unittest.main()