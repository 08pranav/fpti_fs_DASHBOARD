# Railway Deployment Troubleshooting Guide

## Common Railway Deployment Issues & Solutions

### Issue 1: Health Check Failures
**Error**: `replicas never became healthy! Healthcheck failed!`

**Solutions**:

1. **Check Health Endpoint**
   - Ensure `/health` endpoint is accessible
   - Verify the backend is starting properly

2. **Update Environment Variables in Railway**
   ```
   DATABASE_URL=sqlite:///./financial_dashboard.db
   API_HOST=0.0.0.0
   DASH_DEBUG=false
   ALLOWED_ORIGINS=*
   ```

3. **Railway automatically sets PORT** - don't override it

### Issue 2: Service Unavailable
**Error**: `service unavailable`

**Solution**: The app is likely trying to serve both frontend and backend. For Railway, deploy **backend only**:

1. **Use Backend-Only Configuration**
   - Railway config deploys the FastAPI backend
   - Frontend (Dash) should be deployed separately or accessed via API

2. **Environment Variables**
   ```
   PORT=8000  (Railway sets this automatically)
   DATABASE_URL=sqlite:///./financial_dashboard.db
   ALLOWED_ORIGINS=*
   ```

### Issue 3: Port Binding Issues
**Problem**: App not binding to Railway's assigned port

**Solution**: The backend is configured to use `os.getenv("PORT")` which Railway provides automatically.

### Recommended Railway Deployment Steps

#### Option A: Backend-Only Deployment (Recommended)

1. **Deploy Repository**
   - Connect: `https://github.com/08pranav/fpti_fs_DASHBOARD`
   - Railway will detect Dockerfile automatically

2. **Set Environment Variables**
   ```
   DATABASE_URL=sqlite:///./financial_dashboard.db
   ALLOWED_ORIGINS=*
   DASH_DEBUG=false
   ```

3. **Access API**
   - Your Railway URL will serve the FastAPI backend
   - Access API docs at: `https://your-app.railway.app/docs`

#### Option B: Two-Service Deployment

Deploy as **two separate Railway services**:

1. **Backend Service**
   - Repository: Same repo
   - Build Command: `docker build -f Dockerfile.backend .` (create this)
   - Start Command: `python backend/main.py`

2. **Frontend Service**  
   - Repository: Same repo
   - Build Command: `docker build -f Dockerfile.frontend .` (create this)
   - Start Command: `python frontend/dashboard.py`

### Quick Fix Files

#### Create `Dockerfile.backend`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
COPY data/ ./data/
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "backend/main.py"]
```

#### Create `Dockerfile.frontend`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/ ./frontend/
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV API_BASE=https://your-backend-url.railway.app/api
EXPOSE 8050
CMD ["python", "frontend/dashboard.py"]
```

### Alternative: Use Railway Templates

1. **FastAPI Template**
   - Use Railway's FastAPI template as base
   - Copy your backend code into it

2. **Static Frontend**
   - Convert Dash to static files
   - Deploy frontend to Vercel/Netlify
   - Point to Railway backend API

### Testing Locally Before Deploy

```bash
# Test backend only
cd backend
python main.py
# Visit: http://localhost:8000/health

# Test with environment variables
PORT=8000 python backend/main.py
```

### Log Analysis

Check Railway logs for these patterns:

1. **Port binding issues**:
   ```
   ERROR: Address already in use
   ```
   → Make sure app uses `PORT` env var

2. **Health check failures**:
   ```
   Health check failed
   ```
   → Verify `/health` endpoint responds with 200

3. **Import errors**:
   ```
   ModuleNotFoundError
   ```
   → Check requirements.txt includes all dependencies

### Emergency Simple Deploy

If all else fails, create a minimal FastAPI app:

```python
# simple_app.py
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FPTI Financial Dashboard API", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Deploy this first, then gradually add features.