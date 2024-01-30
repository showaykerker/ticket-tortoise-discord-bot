import unittest
from documents import UserModel
import datetime

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = UserModel(
            discord_id=111111111,
            name="John Doe",
            create_date=datetime.datetime.now(),
            last_activate_date=datetime.datetime.now(),
            configs={
                "setting1": True,
                "setting2": 10,
                "setting3": "example",
                "setting4": ["option1", "option2"]
            },
            events_created=[1, 2, 3]
        )

    def test_user_model_initialization(self):
        self.assertEqual(self.user.discord_id, 111111111)
        self.assertEqual(self.user.name, "John Doe")
        self.assertIsNotNone(self.user.create_date)
        self.assertIsNotNone(self.user.last_activate_date)
        self.assertIsInstance(self.user.configs, dict)
        self.assertIsInstance(self.user.events_created, list)

    def test_user_model_overwrite(self):
        self.user.discord_id = 987654321
        self.user.name = "Jane Smith"
        self.user.create_date = datetime.datetime(2022, 1, 1)
        self.user.last_activate_date = datetime.datetime(2022, 1, 2)
        self.user.configs = {
            "setting1": False,
            "setting2": 20,
            "setting3": "updated",
            "setting4": ["option3", "option4"]
        }
        self.user.events_created = [4, 5, 6]

        self.assertEqual(self.user.discord_id, 987654321)
        self.assertEqual(self.user.name, "Jane Smith")
        self.assertEqual(self.user.create_date, datetime.datetime(2022, 1, 1))
        self.assertEqual(self.user.last_activate_date, datetime.datetime(2022, 1, 2))
        self.assertEqual(self.user.configs, {
            "setting1": False,
            "setting2": 20,
            "setting3": "updated",
            "setting4": ["option3", "option4"]
        })
        self.assertEqual(self.user.events_created, [4, 5, 6])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()