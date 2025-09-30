# Mechanic Shop API

Flask API built with Application Factory Pattern and Blueprints.

## 🚀 Setup

```
git clone <repo-url>
cd mechanic_shop_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

⚙️ Run App
```
flask --app run.py run --debug
```

##📌 Endpoints
#Mechanics
- POST /mechanics/ → create mechanic

- GET /mechanics/ → list mechanics

- PUT /mechanics/<id> → update mechanic

- DELETE /mechanics/<id> → delete mechanic

#Service Tickets
- POST /service-tickets/ → create ticket

- GET /service-tickets/ → list tickets

- PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id> → assign mechanic

- PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id> → remove mechanic

