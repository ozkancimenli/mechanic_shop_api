# app/mechanic/routes.py
from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic, MechanicServiceTicket
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema
from sqlalchemy import func
from marshmallow import ValidationError

# CREATE
@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    data = request.get_json() or {}
    try:
        new_mech = mechanic_schema.load(data, session=db.session)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(new_mech)
    db.session.commit()
    return mechanic_schema.jsonify(new_mech), 201


# READ ALL
@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()
    return mechanics_schema.jsonify(mechanics), 200


# UPDATE
@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    data = request.get_json() or {}
    for key, value in data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# DELETE
@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


# POPULAR MECHANICS
@mechanic_bp.route("/popular", methods=["GET"])
def get_popular_mechanics():
    results = (
        db.session.query(Mechanic, func.count(MechanicServiceTicket.id).label("ticket_count"))
        .join(MechanicServiceTicket, Mechanic.id == MechanicServiceTicket.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(MechanicServiceTicket.id).desc())
        .all()
    )

    data = [
        {
            "id": mech.id,
            "name": mech.name,
            "email": mech.email,
            "phone": mech.phone,
            "salary": mech.salary,
            "ticket_count": ticket_count,
        }
        for mech, ticket_count in results
    ]
    return jsonify(data), 200
