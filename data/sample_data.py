import sys
sys.path.append('../backend')

from models import Account, Transaction, Investment, Budget, create_tables, SessionLocal
from datetime import datetime, timedelta
import random
import json

def add_sample_data():
    create_tables()
    db = SessionLocal()

    # Clear existing data
    db.query(Transaction).delete()
    db.query(Account).delete()
    db.query(Investment).delete()
    db.query(Budget).delete()
    db.commit()

    # Add realistic sample accounts
    accounts = [
        Account(name="Chase Checking", account_type="checking", balance=4250.75),
        Account(name="Wells Fargo Savings", account_type="savings", balance=28500.00),
        Account(name="Vanguard 401k", account_type="investment", balance=125000.00),
        Account(name="Fidelity Roth IRA", account_type="investment", balance=42000.00),
        Account(name="Chase Sapphire Credit", account_type="credit", balance=1850.32),
        Account(name="Emergency Fund", account_type="savings", balance=15000.00),
    ]

    for account in accounts:
        db.add(account)
    db.commit()

    # Realistic transaction categories and descriptions
    transaction_templates = {
        "Salary": [
            ("Monthly Salary - Tech Corp", 6500.00),
            ("Bonus Payment", 2000.00),
            ("Freelance Project", 1200.00)
        ],
        "Food": [
            ("Whole Foods Market", -85.50),
            ("Starbucks Coffee", -12.75),
            ("McDonald's", -8.99),
            ("Local Restaurant", -45.00),
            ("Grocery Store", -120.30),
            ("Food Delivery", -25.50)
        ],
        "Transport": [
            ("Gas Station", -55.00),
            ("Uber Ride", -18.50),
            ("Metro Card", -30.00),
            ("Car Insurance", -125.00),
            ("Parking Fee", -15.00)
        ],
        "Entertainment": [
            ("Netflix Subscription", -15.99),
            ("Movie Theater", -28.00),
            ("Spotify Premium", -9.99),
            ("Concert Tickets", -120.00),
            ("Gaming Purchase", -59.99)
        ],
        "Shopping": [
            ("Amazon Purchase", -67.99),
            ("Target", -89.50),
            ("Online Clothing", -125.00),
            ("Electronics Store", -299.99),
            ("Home Depot", -156.75)
        ],
        "Bills": [
            ("Electric Bill", -125.50),
            ("Internet & Cable", -89.99),
            ("Phone Bill", -65.00),
            ("Rent Payment", -2200.00),
            ("Water & Sewer", -45.30),
            ("Insurance Premium", -180.00)
        ],
        "Healthcare": [
            ("Doctor Visit", -150.00),
            ("Pharmacy", -25.99),
            ("Dental Cleaning", -200.00),
            ("Health Insurance", -320.00)
        ],
        "Investment": [
            ("401k Contribution", -750.00),
            ("IRA Contribution", -500.00),
            ("Stock Purchase", -1000.00)
        ]
    }

    # Generate realistic transactions over the past year
    for month_offset in range(12):
        month_start = datetime.now() - timedelta(days=30 * month_offset)

        # Monthly salary
        salary_tx = Transaction(
            account_id=accounts[0].id,  # Checking account
            amount=6500.00,
            description="Monthly Salary - Tech Corp",
            category="Salary",
            date=month_start - timedelta(days=random.randint(0, 5))
        )
        db.add(salary_tx)

        # Regular monthly bills
        for category in ["Bills", "Healthcare"]:
            for desc, amount in transaction_templates[category]:
                if random.random() > 0.3:  # 70% chance of occurrence
                    tx = Transaction(
                        account_id=random.choice(accounts[:2]).id,
                        amount=amount + random.uniform(-10, 10),  # Add some variation
                        description=desc,
                        category=category,
                        date=month_start - timedelta(days=random.randint(0, 28))
                    )
                    db.add(tx)

        # Weekly/frequent transactions
        for week in range(4):
            week_start = month_start - timedelta(days=7 * week)

            # Food transactions (multiple per week)
            for _ in range(random.randint(3, 7)):
                desc, amount = random.choice(transaction_templates["Food"])
                tx = Transaction(
                    account_id=random.choice(accounts[:2]).id,
                    amount=amount + random.uniform(-5, 5),
                    description=desc,
                    category="Food",
                    date=week_start - timedelta(days=random.randint(0, 6))
                )
                db.add(tx)

            # Transport transactions
            if random.random() > 0.2:
                desc, amount = random.choice(transaction_templates["Transport"])
                tx = Transaction(
                    account_id=accounts[0].id,
                    amount=amount + random.uniform(-10, 10),
                    description=desc,
                    category="Transport",
                    date=week_start - timedelta(days=random.randint(0, 6))
                )
                db.add(tx)

        # Monthly shopping and entertainment
        for category in ["Shopping", "Entertainment"]:
            for _ in range(random.randint(2, 5)):
                if transaction_templates[category]:
                    desc, amount = random.choice(transaction_templates[category])
                    tx = Transaction(
                        account_id=random.choice(accounts[:2]).id,
                        amount=amount + random.uniform(-20, 20),
                        description=desc,
                        category=category,
                        date=month_start - timedelta(days=random.randint(0, 28))
                    )
                    db.add(tx)

        # Investment contributions
        if random.random() > 0.1:  # 90% chance monthly
            for desc, amount in transaction_templates["Investment"]:
                if random.random() > 0.4:
                    tx = Transaction(
                        account_id=accounts[2].id,  # Investment account
                        amount=amount,
                        description=desc,
                        category="Investment",
                        date=month_start - timedelta(days=random.randint(0, 28))
                    )
                    db.add(tx)

    # Add diversified investment portfolio
    investments = [
        # Large Cap US Stocks
        Investment(symbol="SPY", shares=120.5, purchase_price=385.00, current_price=421.50),
        Investment(symbol="VTI", shares=85.2, purchase_price=195.00, current_price=218.75),
        Investment(symbol="AAPL", shares=25.0, purchase_price=145.00, current_price=172.50),
        Investment(symbol="MSFT", shares=18.0, purchase_price=280.00, current_price=315.25),
        Investment(symbol="GOOGL", shares=8.5, purchase_price=2200.00, current_price=2450.00),

        # Tech & Growth
        Investment(symbol="QQQ", shares=45.0, purchase_price=325.00, current_price=368.90),
        Investment(symbol="NVDA", shares=12.0, purchase_price=425.00, current_price=485.75),
        Investment(symbol="TSLA", shares=15.0, purchase_price=180.00, current_price=205.30),

        # International & Bonds
        Investment(symbol="VTIAX", shares=200.0, purchase_price=28.50, current_price=31.20),
        Investment(symbol="BND", shares=150.0, purchase_price=82.00, current_price=78.45),
        Investment(symbol="VGIT", shares=75.0, purchase_price=63.50, current_price=61.80),

        # Sector ETFs
        Investment(symbol="VHT", shares=30.0, purchase_price=220.00, current_price=245.60),
        Investment(symbol="VIG", shares=40.0, purchase_price=135.00, current_price=142.85),

        # REITs
        Investment(symbol="VNQ", shares=55.0, purchase_price=88.00, current_price=92.15),
    ]

    for investment in investments:
        db.add(investment)

    # Add comprehensive budget tracking
    current_month = datetime.now().strftime("%Y-%m")
    budgets = [
        Budget(category="Food", monthly_limit=1000, spent=875.50, month=current_month),
        Budget(category="Transport", monthly_limit=400, spent=325.75, month=current_month),
        Budget(category="Entertainment", monthly_limit=300, spent=245.30, month=current_month),
        Budget(category="Shopping", monthly_limit=600, spent=425.99, month=current_month),
        Budget(category="Bills", monthly_limit=2800, spent=2650.79, month=current_month),
        Budget(category="Healthcare", monthly_limit=500, spent=395.99, month=current_month),
        Budget(category="Investment", monthly_limit=2250, spent=2250.00, month=current_month),
    ]

    for budget in budgets:
        db.add(budget)

    # Add previous month's budget for comparison
    prev_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    prev_budgets = [
        Budget(category="Food", monthly_limit=1000, spent=920.25, month=prev_month),
        Budget(category="Transport", monthly_limit=400, spent=380.50, month=prev_month),
        Budget(category="Entertainment", monthly_limit=300, spent=285.75, month=prev_month),
        Budget(category="Shopping", monthly_limit=600, spent=545.30, month=prev_month),
        Budget(category="Bills", monthly_limit=2800, spent=2755.60, month=prev_month),
        Budget(category="Healthcare", monthly_limit=500, spent=150.00, month=prev_month),
        Budget(category="Investment", monthly_limit=2250, spent=2250.00, month=prev_month),
    ]

    for budget in prev_budgets:
        db.add(budget)

    db.commit()
    db.close()
    print("Enhanced sample data added successfully!")
    print(f"Added {len(accounts)} accounts")
    print("Added comprehensive transaction history over 12 months")
    print(f"Added {len(investments)} diverse investments")
    print(f"Added budget tracking for 2 months")

if __name__ == "__main__":
    add_sample_data()