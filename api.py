import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="FPTI Financial Dashboard API",
    version="1.0.0",
    description="A financial dashboard API optimized for Vercel deployment"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory data for demonstration (Vercel is stateless)
SAMPLE_DATA = {
    "net_worth": 125000.50,
    "portfolio_value": 85000.75,
    "monthly_income": [4500, 4800, 5200, 4900, 5100],
    "monthly_expenses": [3200, 3400, 3600, 3300, 3500],
    "months": ["Jan", "Feb", "Mar", "Apr", "May"],
    "transactions": [
        {"id": 1, "amount": 1500.00, "description": "Salary Deposit", "category": "Income", "date": "2025-09-20", "account": "Checking"},
        {"id": 2, "amount": -85.50, "description": "Grocery Store", "category": "Food", "date": "2025-09-19", "account": "Checking"},
        {"id": 3, "amount": -45.00, "description": "Gas Station", "category": "Transportation", "date": "2025-09-18", "account": "Checking"},
        {"id": 4, "amount": 2500.00, "description": "Freelance Project", "category": "Income", "date": "2025-09-17", "account": "Checking"},
        {"id": 5, "amount": -1200.00, "description": "Rent Payment", "category": "Housing", "date": "2025-09-15", "account": "Checking"}
    ],
    "asset_allocation": {
        "Stocks": 60.5,
        "Bonds": 25.0,
        "Cash": 14.5
    },
    "monte_carlo": {
        "percentile_10": 95000,
        "percentile_50": 145000,
        "percentile_90": 210000,
        "current_value": 85000
    }
}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FPTI Financial Dashboard API is running on Vercel", 
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "platform": "vercel"
    }

@app.get("/api/net-worth")
async def get_net_worth():
    """Get current net worth"""
    return {"net_worth": SAMPLE_DATA["net_worth"]}

@app.get("/api/portfolio/value")
async def get_portfolio_value():
    """Get current portfolio value with simulated price updates"""
    # Simulate some price fluctuation
    base_value = SAMPLE_DATA["portfolio_value"]
    fluctuation = random.uniform(-0.02, 0.02)  # ±2% fluctuation
    current_value = base_value * (1 + fluctuation)
    return {"portfolio_value": round(current_value, 2)}

@app.get("/api/cash-flow")
async def get_cash_flow():
    """Get cash flow data"""
    return {
        "income": SAMPLE_DATA["monthly_income"],
        "expenses": SAMPLE_DATA["monthly_expenses"],
        "dates": SAMPLE_DATA["months"]
    }

@app.get("/api/asset-allocation")
async def get_asset_allocation():
    """Get asset allocation data"""
    return SAMPLE_DATA["asset_allocation"]

@app.get("/api/transactions")
async def get_transactions():
    """Get recent transactions"""
    return SAMPLE_DATA["transactions"]

@app.get("/api/monte-carlo")
async def get_monte_carlo():
    """Get Monte Carlo simulation results"""
    return SAMPLE_DATA["monte_carlo"]

@app.get("/api/budget")
async def get_budget():
    """Get budget information"""
    return [
        {"category": "Food", "limit": 800, "spent": 645, "remaining": 155},
        {"category": "Transportation", "limit": 300, "spent": 245, "remaining": 55},
        {"category": "Entertainment", "limit": 200, "spent": 130, "remaining": 70},
        {"category": "Utilities", "limit": 350, "spent": 320, "remaining": 30}
    ]

@app.get("/api/summary")
async def get_summary():
    """Get complete financial summary"""
    return {
        "net_worth": SAMPLE_DATA["net_worth"],
        "portfolio_value": SAMPLE_DATA["portfolio_value"],
        "monthly_income": SAMPLE_DATA["monthly_income"][-1],
        "monthly_expenses": SAMPLE_DATA["monthly_expenses"][-1],
        "total_transactions": len(SAMPLE_DATA["transactions"]),
        "last_updated": datetime.now().isoformat()
    }

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)