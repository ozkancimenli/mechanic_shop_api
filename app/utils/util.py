from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError, ExpiredSignatureError
import os

# ⚠️ Move this to config if possible
SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
ALGORITHM = "HS256"

def encode_token(customer_id: int):
    """Create a JWT token for a customer"""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id),  # must be string
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def token_required(f):
    """Decorator to protect routes with JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = int(data["sub"])
        except ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except JWTError:
            return jsonify({"message": "Invalid token"}), 401

        return f(customer_id, *args, **kwargs)

    return decorated
