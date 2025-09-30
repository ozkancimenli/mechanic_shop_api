from flask import request, jsonify
from app.extensions import db
from app.models import Customer
from . import customer_bp
from .schemas import customer_schema, customers_schema

# CREATE
@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.json
    new_customer = customer_schema.load(data, session=db.session)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# READ ALL
@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = db.session.query(Customer).all()
    return customers_schema.jsonify(customers), 200

# UPDATE
@customer_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
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
