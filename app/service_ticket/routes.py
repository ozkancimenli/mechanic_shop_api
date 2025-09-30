from flask import request, jsonify
from app.extensions import db
from app.models import ServiceTicket, Mechanic, MechanicServiceTicket, Inventory
from . import service_ticket_bp
from .schemas import ticket_schema, tickets_schema

# CREATE
@service_ticket_bp.route("/", methods=["POST"])
def create_ticket():
    data = request.json
    new_ticket = ticket_schema.load(data, session=db.session)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

# READ ALL
@service_ticket_bp.route("/", methods=["GET"])
def get_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return tickets_schema.jsonify(tickets), 200

# ASSIGN MECHANIC
@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mech = db.session.get(Mechanic, mechanic_id)

    if not ticket or not mech:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404

    link = MechanicServiceTicket(mechanic=mech, ticket=ticket)
    db.session.add(link)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mech.id} assigned to ticket {ticket.id}"}), 200

# REMOVE MECHANIC
@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    link = db.session.query(MechanicServiceTicket).filter_by(
        ticket_id=ticket_id, mechanic_id=mechanic_id
    ).first()
    if not link:
        return jsonify({"error": "Relation not found"}), 404

    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}"}), 200

# ADD PART
@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=["PUT"])
def add_part(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket or not part:
        return jsonify({"error": "Ticket or Part not found"}), 404

    if part in ticket.parts:
        return jsonify({"message": "Part already linked to this ticket"}), 400

    ticket.parts.append(part)
    db.session.commit()
    return jsonify({"message": f"Part {part.id} added to ticket {ticket.id}"}), 200

# REMOVE PART
@service_ticket_bp.route("/<int:ticket_id>/remove-part/<int:part_id>", methods=["PUT"])
def remove_part(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket or not part:
        return jsonify({"error": "Ticket or Part not found"}), 404

    if part not in ticket.parts:
        return jsonify({"message": "Part not linked to this ticket"}), 400

    ticket.parts.remove(part)
    db.session.commit()
    return jsonify({"message": f"Part {part.id} removed from ticket {ticket.id}"}), 200

# DELETE
@service_ticket_bp.route("/<int:id>", methods=["DELETE"])
def delete_ticket(id):
    ticket = db.session.get(ServiceTicket, id)
    if not ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket {id} deleted"}), 200
