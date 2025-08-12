Crypto Portfolio Tracker

Overview
A full-stack application to simulate crypto trading with real-time Binance prices.
Users can register/login, add funds, buy/sell assets, and view portfolio analytics such as valuation, profit/loss, and averages.

Backend: FastAPI + SQLAlchemy (SQLite)
Frontend: React + TypeScript + Vite + Tailwind CSS

Features
- JWT authentication (OAuth2 password flow)
- Add virtual funds
- Live price fetch from Binance
- Buy/Sell with transaction history
- Portfolio KPIs and per-asset performance
- Responsive dashboard
- Client/server validation and error handling

Tech Stack
Backend:
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT
- Requests

Frontend:
- React
- TypeScript
- Vite
- Axios
- React Router
- Tailwind CSS

Tooling:
- ESLint
- Tailwind Forms

Project Structure
backend/
  main.py       # API, auth, endpoints
  models.py     # User, Portfolio, Asset, Transaction
  schemas.py    # Pydantic models

frontend/
  src/components    # Login, Register, Dashboard
  src/context       # AuthContext
  src/services      # API client

Getting Started

1) Clone the repository
   git clone <your-repo-url>
   cd crypto-portfolio-tracker

2) Backend (FastAPI)
   cd backend
   python -m venv venv
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   uvicorn main:app --reload
   API available at: http://localhost:8000

3) Frontend (React + Vite)
   cd frontend
   npm install
   npm run dev
   App available at: http://localhost:5173

Environment
- Set SECRET_KEY in backend (replace placeholder in main.py)
- CORS configured to allow local development
- Binance public API used for prices (no API key required)

API Summary
- POST /register
- POST /login → returns JWT
- POST /add-money
- POST /buy
- POST /sell
- GET /portfolio

Security Notes
- Demo only: Passwords are stored in plain text in the current code.
  Use hashing (e.g., passlib/bcrypt) for production.
- Improve error messages and input validation before deployment.

Roadmap
- Password hashing + refresh tokens
- Pagination and detailed transaction view
- Unit/integration tests
- Docker Compose for backend/frontend
- Deploy to cloud (Render/Vercel/Fly.io)
