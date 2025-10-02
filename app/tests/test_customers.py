import unittest
from app import create_app, db

class TestCustomers(unittest.TestCase):
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

    def test_get_customers_empty(self):
        res = self.client.get("/customers/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_customer(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "555-1234",
            "password": "secret123"
        }
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.json)

    def test_create_customer_missing_field(self):
        payload = {"name": "Alice"}  # eksik email, phone, password
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 400)
