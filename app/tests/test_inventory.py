from app.tests.base_test import BaseTestCase

class TestInventory(BaseTestCase):
    def test_get_inventory_empty(self):
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, [])

    def test_create_inventory_item(self):
        payload = {
            "name": "Brake Pad",
            "price": 49.99
        }
        res = self.client.post("/inventory/", json=payload)
        self.assertIn(res.status_code, [201, 400])
