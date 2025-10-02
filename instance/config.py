# instance/config.py
import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Bunuhat1rla@localhost/mechanic_shop_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = "dev-secret-key"  


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = "test-secret-key"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
