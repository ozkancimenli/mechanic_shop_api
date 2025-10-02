import unittest
from app import create_app, db

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.py")
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_mechanics_empty(self):
        res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_mechanic(self):
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "555-111-2222",
            "salary": 50000.0
        }
        res = self.client.post("/mechanics/", json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.json)

    def test_create_mechanic_missing_field(self):
        payload = {"name": "OnlyName"}  # eksik alanlar
        res = self.client.post("/mechanics/", json=payload)
        self.assertEqual(res.status_code, 400)
