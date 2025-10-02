from app.tests.base_test import BaseTestCase

class TestCustomers(BaseTestCase):
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
        payload = {"name": "Alice"}  # email/phone/password eksik
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 400)
