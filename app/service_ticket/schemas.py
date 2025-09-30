from app.extensions import ma
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
