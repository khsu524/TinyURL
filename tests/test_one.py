import unittest
from mock import patch, Mock
from src.routes import app, db

class TestRoutes(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = app.test_client()
    
    def tearDown(self) -> None:
        with app.app_context():
            db.connection.drop_database('my_db')

    @patch("src.routes.shorten", new=Mock(return_value="mocked_shorted"))
    def test_home(self):
        client = self.test_client

        sample_url = "mywebsite"

        res = client.put("/url", 
            data={"long_url": sample_url}
        )
        actual_res = res.json
        self.assertEqual(actual_res['long_url'], sample_url)
        self.assertEqual(actual_res['short_url'], "mocked_shorted")

        res2 = client.get("/url?short_url=mocked_shorted")
        actual_res2 = res2.json
        self.assertEqual(actual_res2, sample_url)

