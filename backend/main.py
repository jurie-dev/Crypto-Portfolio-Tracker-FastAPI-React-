# backend/main.py
from datetime import datetime, timedelta

import jwt
import requests

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base, User, Asset, Portfolio, Transaction
from .schemas import UserCreate, AddMoney, TradeAsset

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB setup
engine = create_engine("sqlite:///./crypto_portfolio.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Use a proper secret in production
SECRET_KEY = "some-key-but-not-this-one"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day for testing


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decode the JWT token (expects payload to contain 'username') and return the User object from DB.
    Raises HTTPException(401) on failure.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str | None = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_crypto_price(symbol: str):
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT", timeout=5)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception:
        return 0.0


@app.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 password flow token endpoint expected by FastAPI's OAuth2PasswordBearer.
    It validates username/password against the DB and returns a JWT (access_token).
    Use this token in the 'Authorize' button as: Bearer <token>
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # simple registration - no duplicate check for brevity (you can add unique constraint handling)
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create portfolio for new user
    portfolio = Portfolio(user_id=db_user.id)
    db.add(portfolio)
    db.commit()

    return {"message": "Successfully created new user."}


@app.post("/add-money")
def add_money(money: AddMoney, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = user.portfolio
    # Ensure portfolio exists
    if not portfolio:
        # create portfolio if missing
        portfolio = Portfolio(user_id=user.id)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

    # If fields are None, initialize them
    if portfolio.total_added_money is None:
        portfolio.total_added_money = 0.0
    if portfolio.available_money is None:
        portfolio.available_money = 0.0

    portfolio.total_added_money += float(money.amount)
    portfolio.available_money += float(money.amount)

    db.commit()
    return {"message": "Successfully added money", "total_added_money": portfolio.total_added_money, "available_money": portfolio.available_money}


@app.post("/buy")
def buy_asset(trade: TradeAsset, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = user.portfolio
    if not portfolio:
        raise HTTPException(status_code=400, detail="User portfolio not found")

    price = get_crypto_price(trade.symbol)
    total_cost = price * trade.quantity

    if total_cost > portfolio.available_money:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    asset = db.query(Asset).filter(Asset.portfolio_id == portfolio.id, Asset.symbol == trade.symbol).first()

    if asset:
        asset.quantity += trade.quantity
    else:
        asset = Asset(portfolio_id=portfolio.id, symbol=trade.symbol, quantity=trade.quantity)
        db.add(asset)

    transaction = Transaction(portfolio_id=portfolio.id, symbol=trade.symbol, quantity=trade.quantity, price=price, timestamp=datetime.utcnow())
    db.add(transaction)

    portfolio.available_money -= total_cost

    db.commit()

    return {"message": "Asset successfully bought."}


@app.post("/sell")
def sell_asset(trade: TradeAsset, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = user.portfolio
    if not portfolio:
        raise HTTPException(status_code=400, detail="User portfolio not found")

    asset = db.query(Asset).filter(Asset.portfolio_id == portfolio.id, Asset.symbol == trade.symbol).first()

    if not asset or asset.quantity < trade.quantity:
        raise HTTPException(status_code=400, detail="Not enough to sell")

    price = get_crypto_price(trade.symbol)
    total_value = price * trade.quantity

    asset.quantity -= trade.quantity

    if asset.quantity <= 0:
        db.delete(asset)

    transaction = Transaction(portfolio_id=portfolio.id, symbol=trade.symbol, quantity=-trade.quantity, price=price, timestamp=datetime.utcnow())
    db.add(transaction)

    portfolio.available_money += total_value

    db.commit()

    return {"message": "Asset successfully sold."}


@app.get("/portfolio")
def get_portfolio(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = user.portfolio
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    assets_response = []
    total_value = portfolio.available_money or 0.0

    for asset in portfolio.assets:
        current_price = get_crypto_price(asset.symbol)
        net_quantity = asset.quantity
        asset_value = current_price * net_quantity
        total_value += asset_value
        transactions = db.query(Transaction).filter(Transaction.portfolio_id == portfolio.id, Transaction.symbol == asset.symbol).all()

        total_cost = 0.0
        total_bought = 0.0

        for t in transactions:
            if t.quantity > 0:
                total_cost += t.quantity * t.price
                total_bought += t.quantity

        avg_purchase_price = total_cost / total_bought if total_bought > 0 else 0.0
        invested_amount = avg_purchase_price * net_quantity

        assets_response.append({
            "symbol": asset.symbol,
            "quantity": asset.quantity,
            "current_price": current_price,
            "total_value": asset_value,
            "avg_purchase_price": avg_purchase_price,
            "performance_abs": asset_value - invested_amount,
            "performance_rel": (asset_value - invested_amount) / invested_amount * 100 if invested_amount != 0 else 0.0
        })

    return {
        "total_added_money": portfolio.total_added_money or 0.0,
        "available_money": portfolio.available_money or 0.0,
        "total_value": total_value,
        "performance_abs": total_value - (portfolio.total_added_money or 0.0),
        "performance_rel": (total_value - (portfolio.total_added_money or 0.0)) / (portfolio.total_added_money or 1) * 100 if (portfolio.total_added_money or 0.0) != 0 else 0.0,
        "assets": assets_response
    }
