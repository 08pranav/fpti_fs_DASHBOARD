# Development Setup Guide for FPTI Financial Dashboard

## Quick Setup

### 1. Clone and Install
```bash
git clone https://github.com/08pranav/fpti_fs_DASHBOARD.git
cd fpti_fs_DASHBOARD
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Database Initialization
```bash
# Initialize database tables
python -c "from backend.models import create_tables; create_tables()"

# Load sample data (optional)
python data/sample_data.py
```

### 4. Run Development Servers

**Option A: Run Both Services**
```bash
./start.sh
```

**Option B: Run Separately (for development)**
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend  
python dashboard.py
```

### 5. Access Application
- Frontend Dashboard: http://localhost:8050
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Project Structure Details

```
fpti_fs_DASHBOARD/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Main application entry
│   └── models.py           # Database models
├── frontend/               # Dash Frontend
│   └── dashboard.py        # Dashboard interface
├── data/                   # Sample data and utilities
│   ├── sample_data.py      # Data generation script
│   └── *.csv              # Sample CSV files
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service setup
├── start.sh              # Startup script
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── railway.json         # Railway deployment config
├── README.md           # Main documentation
├── DEPLOYMENT.md       # Deployment guide
└── LICENSE            # MIT License
```

## API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - Health status
- `GET /docs` - Interactive API documentation

### Financial Data
- `GET /api/net-worth` - Calculate net worth
- `GET /api/portfolio/value` - Portfolio valuation
- `GET /api/cash-flow` - Cash flow analysis
- `GET /api/asset-allocation` - Asset distribution
- `GET /api/transactions` - Recent transactions
- `GET /api/monte-carlo` - Portfolio projections
- `GET /api/budget` - Budget analysis

### Data Upload
- `POST /api/upload/transactions` - Upload transaction CSV
- `POST /api/upload/investments` - Upload investment CSV
- `POST /api/upload/accounts` - Upload account CSV

## Development Tips

### Database Management
```bash
# Reset database
rm backend/financial_dashboard.db
python -c "from backend.models import create_tables; create_tables()"

# Load fresh sample data
python data/sample_data.py
```

### Frontend Development
- Dashboard auto-refreshes every 30 seconds
- Charts update automatically with new data
- Responsive design for mobile/desktop

### Backend Development
- FastAPI auto-reloads on code changes (debug mode)
- SQLAlchemy ORM for database operations
- Async support for improved performance

### Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests (when implemented)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov=frontend
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Issues**
   ```bash
   # Recreate database
   rm backend/financial_dashboard.db
   python -c "from backend.models import create_tables; create_tables()"
   ```

3. **Port Conflicts**
   ```bash
   # Change ports in .env file
   API_PORT=8001
   DASH_PORT=8051
   ```

4. **CORS Issues**
   ```bash
   # Update ALLOWED_ORIGINS in .env
   ALLOWED_ORIGINS=http://localhost:8050,http://127.0.0.1:8050
   ```

### Debug Mode
Enable debug mode for development:
```bash
# In .env file
DASH_DEBUG=true
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Next Steps

1. **Production Deployment**: Follow `DEPLOYMENT.md`
2. **Custom Data**: Replace sample data with real financial data
3. **Authentication**: Implement user authentication system
4. **Real Market Data**: Integrate with financial APIs
5. **Advanced Analytics**: Add more sophisticated financial analysis