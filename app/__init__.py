# app/__init__.py
from flask import Flask
from .extensions import db, ma, limiter, cache
from .models import Base
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp
from .customer import customer_bp
from .inventory import inventory_bp  # ✅ new blueprint

def create_app(config_file="config.py", test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        # 🔑 Testlerden gelen config'i kullan
        app.config.update(test_config)
    else:
        # Normalde instance/config.py'den oku
        app.config.from_pyfile(config_file)

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    with app.app_context():
        Base.metadata.create_all(bind=db.engine)

    # Register Blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # ✅ Swagger UI Setup
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.yml"

    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Shop API"}
    )

    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app
