import os
from app import create_app
from instance.config import DevelopmentConfig, ProductionConfig


def get_config():
    if os.environ.get("PRODUCTION"):  
        return ProductionConfig
    return DevelopmentConfig


app = create_app(config_class=get_config())

if __name__ == "__main__":
    app.run(debug=True)
