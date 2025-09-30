from flask import Blueprint

# Blueprint oluştur
mechanic_bp = Blueprint("mechanic", __name__)

# routes import et (en sonda olmalı yoksa circular import olur)
from . import routes
