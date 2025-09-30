from flask import request, jsonify
from app.extensions import db
from app.models import Mechanic
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema

# CREATE
@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    data = request.json
    new_mech = mechanic_schema.load(data, session=db.session)
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

    data = request.json
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
