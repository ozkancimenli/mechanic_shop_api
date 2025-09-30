from flask import Flask
from .extensions import db, ma
from .models import Base
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp
from .customer import customer_bp

def create_app(config_file="config.py"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        Base.metadata.create_all(bind=db.engine)

    # Register Blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    return app
