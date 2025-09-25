# FPTI Financial Dashboard

A comprehensive financial dashboard application built with FastAPI backend and Dash frontend for managing accounts, transactions, investments, and budgets.

## 🚀 Features

- **Account Management**: Track multiple financial accounts (checking, savings, investment, credit)
- **Transaction Tracking**: Record and categorize financial transactions
- **Investment Portfolio**: Monitor investment performance and holdings
- **Budget Management**: Set and track budget goals
- **Interactive Dashboard**: Real-time visualization of financial data
- **Data Import**: Upload CSV files for bulk data import
- **RESTful API**: Full-featured API for financial data management

## 🏗️ Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: Dash (Python web framework)
- **Database**: SQLite (production-ready with easy migration to PostgreSQL)
- **Data Processing**: Pandas for financial analytics
- **Visualization**: Plotly for interactive charts

## 📁 Project Structure

```
fpti_fs_DASHBOARD/
├── backend/              # FastAPI application
│   ├── main.py          # Main application entry point
│   ├── models.py        # SQLAlchemy database models
│   └── __pycache__/     # Python cache files
├── frontend/            # Dash dashboard application
│   └── dashboard.py     # Main dashboard interface
├── data/               # Sample data and utilities
│   ├── sample_data.py  # Data generation utilities
│   ├── sample_accounts.csv
│   ├── sample_transactions.csv
│   └── sample_investments.csv
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── docker-compose.yml # Multi-service orchestration
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fpti_fs_DASHBOARD.git
   cd fpti_fs_DASHBOARD
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python -c "from backend.models import create_tables; create_tables()"
   ```

6. **Load sample data (optional)**
   ```bash
   python data/sample_data.py
   ```

## 🚀 Running the Application

### Development Mode

1. **Start the Backend API**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend Dashboard** (in a new terminal)
   ```bash
   cd frontend
   python dashboard.py
   ```

3. **Access the application**
   - Frontend Dashboard: http://localhost:8050
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Production Mode (Docker)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Application: http://localhost:8050
   - API: http://localhost:8000

## 🌐 Deployment

### Railway Deployment

This application is configured for easy deployment on Railway:

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard
3. **Deploy** - Railway will automatically detect and deploy both services

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database
DATABASE_URL=sqlite:///./financial_dashboard.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard Configuration
DASH_HOST=0.0.0.0
DASH_PORT=8050
DASH_DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
```

## 📊 API Endpoints

### Accounts
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Create new account
- `GET /api/accounts/{id}` - Get specific account
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Create new transaction
- `GET /api/transactions/{id}` - Get specific transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

### Investments
- `GET /api/investments` - List all investments
- `POST /api/investments` - Create new investment
- `GET /api/investments/{id}` - Get specific investment
- `PUT /api/investments/{id}` - Update investment
- `DELETE /api/investments/{id}` - Delete investment

### Analytics
- `GET /api/analytics/summary` - Financial summary
- `GET /api/analytics/trends` - Spending trends
- `GET /api/analytics/categories` - Category breakdown

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=backend --cov=frontend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Tech Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: Dash
- **Database ORM**: SQLAlchemy
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Deployment**: Docker, Railway
- **Database**: SQLite (development), PostgreSQL (production)

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Real-time stock price integration
- [ ] Mobile responsive design
- [ ] Export reports to PDF/Excel
- [ ] Email notifications for budget alerts
- [ ] Integration with bank APIs
- [ ] Advanced analytics and forecasting
- [ ] Multi-currency support

## 🆘 Support

If you have any questions or need help, please:

1. Check the [documentation](README.md)
2. Search existing [issues](https://github.com/your-username/fpti_fs_DASHBOARD/issues)
3. Create a new issue if needed

---

**Made with ❤️ for better financial management**