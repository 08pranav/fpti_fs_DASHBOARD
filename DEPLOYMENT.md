# FPTI Financial Dashboard - Deployment Guide

## Quick Start (Local Development)

1. **Clone and setup**
   ```bash
   git clone https://github.com/your-username/fpti_fs_DASHBOARD.git
   cd fpti_fs_DASHBOARD
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   # Terminal 1: Start Backend
   cd backend && python main.py

   # Terminal 2: Start Frontend
   cd frontend && python dashboard.py
   ```

3. **Access the app**
   - Dashboard: http://localhost:8050
   - API: http://localhost:8000/docs

## Railway Deployment

### Method 1: Automatic Deployment (Recommended)

1. **Connect GitHub to Railway**
   - Push this code to your GitHub repository
   - Connect your GitHub account to Railway
   - Import the repository

2. **Environment Variables**
   Set these in Railway dashboard:
   ```
   DATABASE_URL=sqlite:///./financial_dashboard.db
   API_HOST=0.0.0.0
   API_PORT=8000
   DASH_HOST=0.0.0.0
   DASH_PORT=8050
   DASH_DEBUG=false
   ALLOWED_ORIGINS=*
   ```

3. **Deploy**
   - Railway will automatically detect the Dockerfile
   - The app will be available at your Railway-provided URL

### Method 2: Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

## Docker Deployment

1. **Build and run**
   ```bash
   docker-compose up --build
   ```

2. **Access**
   - Application: http://localhost:8050
   - API: http://localhost:8000

## Environment Configuration

Create `.env` file:
```env
# Copy from .env.example and modify as needed
DATABASE_URL=sqlite:///./financial_dashboard.db
API_HOST=0.0.0.0
API_PORT=8000
DASH_HOST=0.0.0.0
DASH_PORT=8050
DASH_DEBUG=false
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=*
```

## Production Considerations

### Security
- Change `SECRET_KEY` in production
- Restrict `ALLOWED_ORIGINS` to your domain
- Use PostgreSQL instead of SQLite for production
- Implement proper authentication

### Performance
- Use PostgreSQL or similar production database
- Add Redis for caching
- Implement connection pooling
- Use reverse proxy (nginx)

### Monitoring
- Add logging configuration
- Implement health checks
- Set up error tracking (Sentry)
- Monitor resource usage

## Troubleshooting

### Common Issues

1. **Port conflicts**
   - Change ports in `.env` file
   - Ensure ports are available

2. **Database issues**
   - Check DATABASE_URL
   - Ensure write permissions
   - Initialize database if needed

3. **API connection errors**
   - Verify backend is running
   - Check API_BASE URL in frontend
   - Ensure CORS is configured

### Logs

Check application logs:
```bash
# Docker logs
docker-compose logs -f

# Local development
# Check terminal outputs for errors
```

## Support

For issues:
1. Check this deployment guide
2. Review application logs
3. Create GitHub issue with details