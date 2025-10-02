## Mechanic Shop API

Flask REST API built with **Application Factory Pattern**, **Blueprints**, and **SQLAlchemy ORM**.  
Implements **Mechanics, Customers, Service Tickets, Inventory**, and a modeled junction table (`MechanicServiceTicket`).  

## 🌐 Live Demo
- Base URL: [https://mechanic-shop-api-hf0y.onrender.com](https://mechanic-shop-api-hf0y.onrender.com)  
- Swagger UI: [https://mechanic-shop-api-hf0y.onrender.com/swagger](https://mechanic-shop-api-hf0y.onrender.com/swagger)

---

## 🚀 Features
- 🔐 JWT authentication for customers  
- ⚡ Rate limiting with **Flask-Limiter**  
- 🗃️ Caching with **Flask-Caching**  
- 📊 Popular mechanics query  
- 🧩 Many-to-Many with parts (inventory ↔ service tickets)  
- 📑 Swagger documentation (host updated to live API + HTTPS)  
- ✅ Unit testing with `unittest`  

---

## 🛠️ Local Setup (Development)

```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Run app locally:
```
python flask_app.py
```
Local database (MySQL) is configured in instance/config.py.

## 🌐 Deployment (Production - Render)
# Procfile
```
web: gunicorn flask_app:app
```
# Environment Variables (Render Dashboard → Environment)
```
SQLALCHEMY_DATABASE_URI=<your Render PostgreSQL URL>
SECRET_KEY=<your_secret_key>
PRODUCTION=1
```
# Config (instance/config.py)
- DevelopmentConfig → MySQL (local)
- ProductionConfig → PostgreSQL (Render, env vars)

## ⚙️ CI/CD Pipeline
- GitHub Actions workflow: .github/workflows/main.yml
- Steps:
    - Install dependencies
    - Run unit tests
    - Deploy to Render (if tests pass)
- Secrets (stored in GitHub Repo → Settings → Secrets):
    - RENDER_API_KEY
    - SERVICE_ID

## 📌 Example Endpoints
- POST /mechanics/ → create mechanic
- GET /customers/ → list customers
- POST /customers/login → login (returns JWT)
- GET /customers/my-tickets → get tickets (Bearer token required)
- POST /inventory/ → create part

## 🧪 Example cURL Test
```
curl -X GET https://mechanic-shop-api-hf0y.onrender.com/mechanics/
```
## 📑 Documentation & Testing
- Swagger UI: /swagger
- Run tests locally:
```
python -m unittest discover -s app/tests -p "test_*.py"
```
