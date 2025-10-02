import os
from app import create_app
from instance.config import DevelopmentConfig, ProductionConfig

# Prod mu Dev mi seç
def get_config():
    if os.environ.get("PRODUCTION"):  # Render'da PRODUCTION=1 set edilecek
        return ProductionConfig
    return DevelopmentConfig

app = create_app(get_config())

if __name__ == "__main__":
    app.run(debug=True)
