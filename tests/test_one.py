import unittest
from routes import app, db

class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = app.test_client()
    
    def tearDown(self) -> None:
        with app.app_context():
            db.connection.drop_database('my_db')

    def test_home(self):
        client = self.test_client

        sample_url = "mywebsite"

        res = client.put("/url", 
            data={"long_url": sample_url}
        )
        actual_res = res.json
        self.assertEqual(actual_res['long_url'], sample_url)
        self.assertEqual(actual_res['short_url'], "SHORT_URL")

        res2 = client.get("/url?short_url=SHORT_URL")
        actual_res2 = res2.json
        self.assertEqual(actual_res2, "LONGGGG")

