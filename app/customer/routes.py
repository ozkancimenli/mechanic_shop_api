from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import Customer, ServiceTicket
from . import customer_bp
from .schemas import customer_schema, customers_schema
from app.utils.util import encode_token, token_required

# CREATE
@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.json
    # hash password
    if "password" in data:
        data["password"] = generate_password_hash(data["password"])
    new_customer = customer_schema.load(data, session=db.session)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# LOGIN
@customer_bp.route("/login", methods=["POST"])
def login_customer():
    creds = request.json or {}
    email = creds.get("email")
    password = creds.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    customer = Customer.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        token = encode_token(customer.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email
            },
            "token": token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401

# READ ALL (with pagination)
@customer_bp.route("/", methods=["GET"])
def get_customers():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    customers = Customer.query.offset(offset).limit(limit).all()
    return customers_schema.jsonify(customers), 200

# GET OWN TICKETS (protected)
@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return jsonify([{
        "id": t.id,
        "VIN": t.VIN,
        "service_date": t.service_date,
        "service_desc": t.service_desc
    } for t in tickets]), 200

# UPDATE
@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        if key == "password":
            value = generate_password_hash(value)
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# DELETE
@customer_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted"}), 200
