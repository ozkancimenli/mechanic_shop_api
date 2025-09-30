##Mechanic Shop API

Flask REST API built with Application Factory Pattern, Blueprints, and SQLAlchemy ORM.
Implements Mechanics, Customers, and Service Tickets with a modeled junction table (MechanicServiceTicket) that stores assignment metadata (e.g., start_date).

##🚀 Setup
```
git clone <repo-url>
cd mechanic_shop_api
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#⚙️ Run App
```

flask --app run.py run --debug
```


Or simply:
```

python run.py
```

#🗄️ Database

- Default DB connection: MySQL (instance/config.py)

- Update credentials before running.

- On first run, tables are created automatically from SQLAlchemy models.

##📌 Endpoints
#Mechanics

- POST /mechanics/ → create mechanic

- GET /mechanics/ → list mechanics

- PUT /mechanics/<id> → update mechanic

- DELETE /mechanics/<id> → delete mechanic

#Service Tickets

- POST /service-tickets/ → create ticket

- GET /service-tickets/ → list tickets

- PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> → assign mechanic (creates junction row with start_date)

- PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id> → remove mechanic from ticket

- DELETE /service-tickets/<id> → delete ticket

#Customers

- POST /customers/ → create customer

- GET /customers/ → list customers

- PUT /customers/<id> → update customer

- DELETE /customers/<id> → delete customer

##🔗 Junction Table Behavior

The API uses a modeled junction table:
```
class MechanicServiceTicket(Base):
    __tablename__ = "mechanic_service_tickets"
    mechanic_id
    ticket_id
    start_date
```

When assigning a mechanic to a ticket:

- A new row in mechanic_service_tickets is created.

- start_date is automatically recorded.

When removing:

- The corresponding row is deleted.

##🛠️ Example Requests
#Create Mechanic
```
POST /mechanics/
{
  "name": "Ali",
  "email": "ali@example.com",
  "phone": "555-111-2222",
  "salary": 4500
}
```

#Create Ticket
```
POST /service-tickets/
{
  "VIN": "123456789",
  "service_date": "2025-09-30",
  "service_desc": "Oil change",
  "customer_id": 1
}
```

#Assign Mechanic
```
PUT /service-tickets/1/assign-mechanic/2
```