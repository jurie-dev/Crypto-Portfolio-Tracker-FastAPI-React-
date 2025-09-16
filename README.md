Crypto Portfolio Tracker – Backend
Overview

This is a FastAPI backend that simulates crypto trading with real-time Binance prices.
Users can register/login, add funds, buy/sell assets, and view portfolio analytics such as valuation, profit/loss, and averages.

The backend exposes a REST API with JWT authentication and SQLite persistence.
You can interact with it directly via Swagger UI or API clients (Postman, curl, etc.).

Features

JWT authentication (OAuth2 password flow)

Register/login users

Add virtual funds to a portfolio

Fetch live prices from Binance

Buy/sell crypto assets with transaction history

Portfolio KPIs and per-asset performance

Automatic Swagger UI documentation at /docs

Tech Stack

FastAPI (API framework)

SQLAlchemy (ORM)

SQLite (lightweight database)

PyJWT (JWT-based authentication)

Requests (for Binance price fetches)

Project Structure
backend/
  main.py       # API, authentication, and endpoints
  models.py     # Database models (User, Portfolio, Asset, Transaction)
  schemas.py    # Pydantic request/response models
  crypto_portfolio.db  # SQLite database (auto-created)

Getting Started
1. Clone the repository
git clone <your-repo-url>
cd crypto-portfolio-tracker/backend

2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the server
uvicorn main:app --reload --port 8000


API available at: http://localhost:8000

Interactive docs: http://localhost:8000/docs

API Summary

POST /register → Create new user

POST /token → OAuth2 login (returns JWT)

POST /login → Alternative login endpoint (returns JWT)

POST /add-money → Add funds to user’s portfolio

POST /buy → Buy crypto assets

POST /sell → Sell crypto assets

GET /portfolio → View portfolio with KPIs and performance

Environment

SECRET_KEY in main.py is used for JWT signing. Replace the placeholder before production.

CORS is configured to allow local testing.

Prices are fetched from Binance public API (no API key required).

Security Notes

Passwords are stored in plain text → not safe for production.
Use hashing (e.g., passlib[bcrypt]) before deploying.

Error handling and input validation should be improved for production-grade security.

Roadmap

Implement password hashing and refresh tokens

Add pagination and detailed transaction history

Unit and integration tests

Dockerize the backend

Deploy to cloud platforms (Render, Fly.io, etc.)
