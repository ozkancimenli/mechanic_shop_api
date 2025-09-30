from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema

# CREATE
@inventory_bp.route("/", methods=["POST"])
def create_part():
    try:
        data = inventory_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(data)
    db.session.commit()
    return inventory_schema.jsonify(data), 201

# READ ALL
@inventory_bp.route("/", methods=["GET"])
def get_parts():
    parts = Inventory.query.order_by(Inventory.id.desc()).all()
    return inventories_schema.jsonify(parts), 200

# READ ONE
@inventory_bp.route("/<int:part_id>", methods=["GET"])
def get_part(part_id):
    part = Inventory.query.get_or_404(part_id)
    return inventory_schema.jsonify(part), 200

# UPDATE
@inventory_bp.route("/<int:part_id>", methods=["PUT"])
def update_part(part_id):
    part = Inventory.query.get_or_404(part_id)
    payload = request.json or {}

    if "name" in payload:
        part.name = payload["name"]
    if "price" in payload:
        part.price = payload["price"]

    db.session.commit()
    return inventory_schema.jsonify(part), 200

# DELETE
@inventory_bp.route("/<int:part_id>", methods=["DELETE"])
def delete_part(part_id):
    part = Inventory.query.get_or_404(part_id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {part_id} deleted"}), 200
