from flask import request, jsonify
from app.extensions import db, limiter, cache
from app.models import Inventory, ServiceTicket
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema

# CREATE
@inventory_bp.route("/", methods=["POST"])
@limiter.limit("20 per hour")
def create_inventory():
    data = request.json
    new_part = inventory_schema.load(data, session=db.session)
    db.session.add(new_part)
    db.session.commit()
    cache.clear()
    return inventory_schema.jsonify(new_part), 201

# READ ALL
@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_inventory():
    parts = db.session.query(Inventory).all()
    return inventories_schema.jsonify(parts), 200

# GET ONE
@inventory_bp.route("/<int:id>", methods=["GET"])
def get_inventory_item(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    return inventory_schema.jsonify(part), 200

# UPDATE
@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_inventory(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    data = request.json
    for key, value in data.items():
        setattr(part, key, value)

    db.session.commit()
    cache.clear()
    return inventory_schema.jsonify(part), 200

# DELETE
@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_inventory(id):
    part = db.session.get(Inventory, id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()
    cache.clear()
    return jsonify({"message": f"Part {id} deleted"}), 200

# ADD PART TO TICKET
@inventory_bp.route("/add-to-ticket/<int:ticket_id>/<int:part_id>", methods=["PUT"])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket or not part:
        return jsonify({"error": "Ticket or Part not found"}), 404

    if part in ticket.parts:
        return jsonify({"message": "Part already assigned"}), 409

    ticket.parts.append(part)
    db.session.commit()
    return jsonify({"message": f"Part {part.id} added to ticket {ticket.id}"}), 200
    