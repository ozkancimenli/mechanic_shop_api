# flask_app.py
from app import create_app
import os

def get_config():

    if os.environ.get("PRODUCTION"):
        return "ProductionConfig"
    return "config.py"

app = create_app(get_config())

if __name__ == "__main__":

    app.run(debug=True)
