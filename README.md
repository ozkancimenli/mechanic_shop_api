## Mechanic Shop API

Flask REST API built with **Application Factory Pattern**, **Blueprints**, and **SQLAlchemy ORM**.  
Implements **Mechanics, Customers, Service Tickets, Inventory**, and a modeled junction table (`MechanicServiceTicket`) that stores assignment metadata (e.g., `start_date`).  

Supports:  
- 🔐 JWT authentication for customers (`/login`, `/my-tickets`)  
- ⚡ Rate limiting with **Flask-Limiter**  
- 🗃️ Caching with **Flask-Caching**  
- 📊 Popular mechanics query  
- 🧩 Many-to-Many with parts (inventory ↔ service tickets)  

---

## 🚀 Setup

```
git clone <repo-url>
cd mechanic_shop_api
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## ⚙️ Run App
```
flask --app run.py run --debug
```
Or simply:
```
python run.py
```

## 🗄️ Database
- Default DB connection: MySQL (instance/config.py)
- Update credentials before running.
- On first run, tables are created automatically from SQLAlchemy models.

## 📌 Endpoints
# Mechanics
- POST /mechanics/ → create mechanic
- GET /mechanics/ → list mechanics
- PUT /mechanics/<id> → update mechanic
- DELETE /mechanics/<id> → delete mechanic
- GET /mechanics/popular → mechanics ordered by most tickets

# Service Tickets
- POST /service-tickets/ → create ticket
- GET /service-tickets/ → list tickets
- PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> → assign mechanic (creates junction row with start_date)
- PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id> → remove mechanic from ticket
- PUT /service-tickets/<ticket_id>/add-part/<part_id> → add part to ticket
- PUT /service-tickets/<ticket_id>/remove-part/<part_id> → remove part from ticket
- DELETE /service-tickets/<id> → delete ticket

# Customers
- POST /customers/ → create customer
- POST /customers/login → login, returns JWT token
- GET /customers/ → list customers (supports limit & offset pagination)
- GET /customers/my-tickets → get own tickets (requires Bearer token)
- PUT /customers/<id> → update customer (password hashed)
- DELETE /customers/<id> → delete customer

# Inventory
- POST /inventory/ → create part
- GET /inventory/ → list all parts (cached)
- GET /inventory/<id> → get part by id
- PUT /inventory/<id> → update part
- DELETE /inventory/<id> → delete part
- PUT /inventory/add-to-ticket/<ticket_id>/<part_id> → add part to ticket

## 🔗 Junction Table Behavior
The API uses a modeled junction table:
```
class MechanicServiceTicket(Base):
    __tablename__ = "mechanic_service_tickets"
    mechanic_id
    ticket_id
    start_date
```
- Assigning a mechanic → new row with start_date.
- Removing a mechanic → row is deleted.

## 🛠️ Example Requests
# Create Mechanic
```
POST /mechanics/
{
  "name": "Ali",
  "email": "ali@example.com",
  "phone": "555-111-2222",
  "salary": 4500
}
```
# Create Ticket
```
POST /service-tickets/
{
  "VIN": "123456789",
  "service_date": "2025-09-30",
  "service_desc": "Oil change",
  "customer_id": 1
}
```
# Assign Mechanic
```
PUT /service-tickets/1/assign-mechanic/2
```
Login Customer
```
POST /customers/login
{
  "email": "jane@example.com",
  "password": "secret"
}
```
Response:
```
{
  "status": "success",
  "token": "<JWT_TOKEN>"
}
```
Use this token in Authorization header:
Authorization: Bearer <JWT_TOKEN>

## 📦 Postman Collection
A ready-to-use Postman collection is included:
```
postman/collections/mechanic-shop.json
```
To use:
1. Open Postman → Import
2. Select the file → all requests are preloaded
3. Update {{base_url}} and {{token}} variables as needed
