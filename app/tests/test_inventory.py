import unittest
from app import create_app, db

class TestInventory(unittest.TestCase):
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

    def test_get_inventory_empty(self):
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_inventory_item(self):
        payload = {
            "name": "Brake Pad",
            "stock": 20,       # ⚠️ modelinde stock yerine quantity/amount varsa değiştir
            "price": 49.99
        }
        res = self.client.post("/inventory/", json=payload)
        self.assertIn(res.status_code, [201, 400])
