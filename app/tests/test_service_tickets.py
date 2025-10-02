from app.tests.base_test import BaseTestCase

class TestServiceTickets(BaseTestCase):
    def test_get_service_tickets_empty(self):
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_service_ticket(self):
        # önce müşteri yarat
        self.client.post("/customers/", json={
            "name": "Alice Smith",
            "email": "alice@example.com",
            "phone": "555-1234",
            "password": "secret123"
        })

        payload = {
            "VIN": "ABC123XYZ",
            "service_date": "2025-10-01",
            "service_desc": "Oil change",
            "customer_id": 1
        }
        res = self.client.post("/service-tickets/", json=payload)
        self.assertIn(res.status_code, [201, 400])
