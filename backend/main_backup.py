import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import pandas as pd
import asyncio
import random
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models import (
    Account, Transaction, Investment, Budget,
    get_db, create_tables, SessionLocal
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "FPTI Financial Dashboard API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="A comprehensive financial dashboard API for managing accounts, transactions, and investments"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
create_tables()

class FinancialAnalyzer:
    def __init__(self, db: Session):
        self.db = db

    def get_net_worth(self) -> float:
        accounts = self.db.query(Account).all()
        total_assets = sum(acc.balance for acc in accounts if acc.account_type != "credit")
        total_liabilities = sum(acc.balance for acc in accounts if acc.account_type == "credit")

        investments = self.db.query(Investment).all()
        investment_value = sum(inv.shares * inv.current_price for inv in investments)

        return total_assets + investment_value - total_liabilities

    def get_portfolio_value(self) -> float:
        investments = self.db.query(Investment).all()
        return sum(inv.shares * inv.current_price for inv in investments)

    def get_cash_flow_data(self) -> Dict:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        transactions = self.db.query(Transaction).filter(
            Transaction.date >= start_date
        ).all()

        df = pd.DataFrame([{
            'date': t.date,
            'amount': t.amount,
            'category': t.category
        } for t in transactions])

        if df.empty:
            return {'income': [], 'expenses': [], 'dates': []}

        df['month'] = df['date'].dt.to_period('M')
        monthly_data = df.groupby('month')['amount'].sum().reset_index()

        income = [max(0, amount) for amount in monthly_data['amount']]
        expenses = [abs(min(0, amount)) for amount in monthly_data['amount']]
        dates = [str(month) for month in monthly_data['month']]

        return {'income': income, 'expenses': expenses, 'dates': dates}

async def fetch_market_data(symbol: str) -> float:
    """Simulate market data fetch - in production, integrate with real API"""
    await asyncio.sleep(0.1)  # Simulate API call delay
    return round(random.uniform(50, 500), 2)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "FPTI Financial Dashboard API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/portfolio/value")
async def get_portfolio_value(db: Session = Depends(get_db)):
    analyzer = FinancialAnalyzer(db)

    # Update investment prices with async calls
    investments = db.query(Investment).all()
    for investment in investments:
        investment.current_price = await fetch_market_data(investment.symbol)
    db.commit()

    return {"portfolio_value": analyzer.get_portfolio_value()}

@app.get("/api/net-worth")
def get_net_worth(db: Session = Depends(get_db)):
    analyzer = FinancialAnalyzer(db)
    return {"net_worth": analyzer.get_net_worth()}

@app.get("/api/transactions")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).limit(100).all()
    return [{
        "id": t.id,
        "amount": t.amount,
        "description": t.description,
        "category": t.category,
        "date": t.date.isoformat(),
        "account": t.account.name
    } for t in transactions]

@app.get("/api/cash-flow")
def get_cash_flow(db: Session = Depends(get_db)):
    analyzer = FinancialAnalyzer(db)
    return analyzer.get_cash_flow_data()

@app.get("/api/asset-allocation")
def get_asset_allocation(db: Session = Depends(get_db)):
    investments = db.query(Investment).all()

    allocation = {}
    total_value = 0

    for inv in investments:
        value = inv.shares * inv.current_price
        total_value += value

        if inv.symbol.startswith('BOND'):
            allocation['Bonds'] = allocation.get('Bonds', 0) + value
        elif inv.symbol in ['SPY', 'VTI', 'QQQ']:
            allocation['Stocks'] = allocation.get('Stocks', 0) + value
        else:
            allocation['Other'] = allocation.get('Other', 0) + value

    # Convert to percentages
    if total_value > 0:
        for key in allocation:
            allocation[key] = round((allocation[key] / total_value) * 100, 2)

    return allocation

@app.get("/api/monte-carlo")
def get_monte_carlo(db: Session = Depends(get_db)):
    analyzer = FinancialAnalyzer(db)
    current_value = analyzer.get_portfolio_value()

    # Simple Monte Carlo simulation
    years = 10
    simulations = 1000
    results = []

    for _ in range(simulations):
        value = current_value
        for year in range(years):
            # Simulate annual returns (normal distribution around 7% with 15% volatility)
            annual_return = random.gauss(0.07, 0.15)
            value *= (1 + annual_return)
        results.append(value)

    results.sort()
    return {
        "percentile_10": round(results[int(0.1 * len(results))], 2),
        "percentile_50": round(results[int(0.5 * len(results))], 2),
        "percentile_90": round(results[int(0.9 * len(results))], 2),
        "current_value": current_value
    }

@app.get("/api/budget")
def get_budget(db: Session = Depends(get_db)):
    current_month = datetime.now().strftime("%Y-%m")
    budgets = db.query(Budget).filter(Budget.month == current_month).all()

    return [{
        "category": b.category,
        "limit": b.monthly_limit,
        "spent": b.spent,
        "remaining": b.monthly_limit - b.spent
    } for b in budgets]

@app.post("/api/upload/transactions")
async def upload_transactions_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload transactions from CSV file
    Expected columns: date, amount, description, category, account_name
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Validate required columns
        required_columns = ['date', 'amount', 'description', 'category', 'account_name']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )

        # Process each row
        added_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # Find or create account
                account = db.query(Account).filter(Account.name == row['account_name']).first()
                if not account:
                    # Create new account if it doesn't exist
                    account = Account(
                        name=row['account_name'],
                        account_type='checking',  # Default type
                        balance=0.0
                    )
                    db.add(account)
                    db.commit()
                    db.refresh(account)

                # Parse date
                transaction_date = pd.to_datetime(row['date']).to_pydatetime()

                # Create transaction
                transaction = Transaction(
                    account_id=account.id,
                    amount=float(row['amount']),
                    description=row['description'],
                    category=row['category'],
                    date=transaction_date
                )
                db.add(transaction)
                added_count += 1

            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully uploaded {added_count} transactions",
            "added_count": added_count,
            "errors": errors[:10] if errors else []  # Limit to first 10 errors
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.post("/api/upload/investments")
async def upload_investments_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload investments from CSV file
    Expected columns: symbol, shares, purchase_price, current_price, purchase_date
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Validate required columns
        required_columns = ['symbol', 'shares', 'purchase_price', 'current_price', 'purchase_date']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )

        # Process each row
        added_count = 0
        updated_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # Parse date
                purchase_date = pd.to_datetime(row['purchase_date']).to_pydatetime()

                # Check if investment already exists
                existing = db.query(Investment).filter(Investment.symbol == row['symbol']).first()

                if existing:
                    # Update existing investment
                    existing.shares = float(row['shares'])
                    existing.purchase_price = float(row['purchase_price'])
                    existing.current_price = float(row['current_price'])
                    existing.purchase_date = purchase_date
                    updated_count += 1
                else:
                    # Create new investment
                    investment = Investment(
                        symbol=row['symbol'],
                        shares=float(row['shares']),
                        purchase_price=float(row['purchase_price']),
                        current_price=float(row['current_price']),
                        purchase_date=purchase_date
                    )
                    db.add(investment)
                    added_count += 1

            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully processed {added_count + updated_count} investments",
            "added_count": added_count,
            "updated_count": updated_count,
            "errors": errors[:10] if errors else []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.post("/api/upload/accounts")
async def upload_accounts_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload accounts from CSV file
    Expected columns: name, account_type, balance
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Validate required columns
        required_columns = ['name', 'account_type', 'balance']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )

        # Process each row
        added_count = 0
        updated_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                # Check if account already exists
                existing = db.query(Account).filter(Account.name == row['name']).first()

                if existing:
                    # Update existing account
                    existing.account_type = row['account_type']
                    existing.balance = float(row['balance'])
                    updated_count += 1
                else:
                    # Create new account
                    account = Account(
                        name=row['name'],
                        account_type=row['account_type'],
                        balance=float(row['balance'])
                    )
                    db.add(account)
                    added_count += 1

            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully processed {added_count + updated_count} accounts",
            "added_count": added_count,
            "updated_count": updated_count,
            "errors": errors[:10] if errors else []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DASH_DEBUG", "False").lower() == "true"
    
    uvicorn.run(app, host=host, port=port, reload=debug)