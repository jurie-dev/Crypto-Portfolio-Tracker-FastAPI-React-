Crypto Portfolio Tracker - Backend
==================================

Overview
--------
This is the backend of the Crypto Portfolio Tracker project.  
It simulates crypto trading with real-time Binance prices.  
Users can register, login, add funds, buy/sell assets, and view portfolio analytics such as valuation, profit/loss, and averages.

Backend Tech Stack
------------------
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT
- Requests

Features
--------
- JWT authentication (OAuth2 password flow)
- Add virtual funds
- Live price fetch from Binance
- Buy/Sell with transaction history
- Portfolio KPIs and per-asset performance
- Client/server validation and error handling

Project Structure
-----------------
backend/
  main.py       -> API, authentication, endpoints
  models.py     -> User, Portfolio, Asset, Transaction
  schemas.py    -> Pydantic models

Getting Started
---------------
1) Clone the repository
   git clone <your-repo-url>
   cd crypto-portfolio-tracker/backend

2) Create virtual environment
   python -m venv venv

3) Activate virtual environment
   Windows:
     venv\Scripts\activate
   macOS/Linux:
     source venv/bin/activate

4) Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt

5) Run FastAPI backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

API Access
----------
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:      http://127.0.0.1:8000/redoc

Security Notes
--------------
- Demo only: Passwords are stored in plain text in the current code.
- Use hashing (e.g., passlib/bcrypt) for production.
- Improve error messages and input validation before deployment.

Roadmap
-------
- Add password hashing and refresh tokens
- Pagination and detailed transaction view
- Unit/integration tests
- Docker Compose for backend
- Deploy to cloud (Render, Fly.io, etc.)
