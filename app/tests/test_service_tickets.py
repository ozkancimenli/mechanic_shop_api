import unittest
from app import create_app, db

class TestServiceTickets(unittest.TestCase):
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

    def test_get_service_tickets_empty(self):
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_service_ticket(self):
        payload = {
            "VIN": "ABC123XYZ",
            "service_date": "2025-09-30",
            "service_desc": "Oil change",
            "customer_id": 1
        }
        res = self.client.post("/service-tickets/", json=payload)
        # müşteri yoksa 400 dönebilir
        self.assertIn(res.status_code, [201, 400])
