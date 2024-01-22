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

    def test_mongo_connection_create_user_request(self):
        # Test case for creating a user request
        user_id = 123456789
        request_link = "https://example.com/request"
        has_user_request = self.mongo.has_user_request(request_link)
        self.assertFalse(has_user_request)

        result = self.mongo.create_user_request(user_id, request_link)
        result_exists = self.mongo.db.user_requests.find_one({"request_link": request_link+"/"})
        self.assertTrue(result)
        self.assertFalse(result_exists)

        has_user_request = self.mongo.has_user_request(request_link)
        self.assertTrue(has_user_request)

        request = self.mongo.db.user_requests.find_one({"request_link": request_link})
        self.assertIsNotNone(request)
        self.assertEqual(request["user_id"], user_id)
        self.assertEqual(request["request_link"], request_link)
        self.assertFalse(request["fulfilled"])

    def tearDown(self):
        self.mongo.db.users.delete_many({})
        self.mongo.db.user_requests.delete_many({})

if __name__ == '__main__':
    unittest.main()