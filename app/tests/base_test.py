# app/tests/base_test.py
import unittest
from app import create_app
from app.extensions import db
from app.models import Base

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # 🔑 create_app'a test_config gönderiyoruz
        self.app = create_app(test_config={
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.engine.dispose()
            Base.metadata.create_all(bind=db.engine)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            Base.metadata.drop_all(bind=db.engine)
            db.engine.dispose()
