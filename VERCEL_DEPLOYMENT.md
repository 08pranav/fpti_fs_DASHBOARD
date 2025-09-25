# Vercel Deployment Guide for FPTI Financial Dashboard

## 📋 Overview

This project can be deployed to **Vercel** as a serverless FastAPI application. The deployment has been optimized for Vercel's serverless functions.

## 🚀 Quick Vercel Deployment

### Method 1: Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)**
2. **Connect GitHub** and import repository: `08pranav/fpti_fs_DASHBOARD`
3. **Deploy** - Vercel will automatically detect the configuration
4. **Access your API** at: `https://your-project.vercel.app`

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## 📁 Vercel-Optimized Structure

```
fpti_fs_DASHBOARD/
├── main.py              # Vercel entry point
├── api.py               # Optimized FastAPI app
├── vercel.json          # Vercel configuration
├── requirements.txt     # Minimal dependencies
└── requirements_full.txt # Complete dependencies (for local dev)
```

## 🔧 What's Different for Vercel

### **Simplified Architecture**
- **API Only**: Vercel deployment serves the FastAPI backend
- **In-Memory Data**: Uses sample data (Vercel functions are stateless)
- **Minimal Dependencies**: Reduced package size for faster cold starts

### **Key Files for Vercel**
1. **`main.py`**: Entry point that Vercel expects
2. **`api.py`**: Lightweight FastAPI application
3. **`vercel.json`**: Deployment configuration
4. **`requirements.txt`**: Minimal dependencies for Vercel

## 🌐 API Endpoints (Vercel Deployment)

Once deployed, your Vercel URL will serve these endpoints:

### **Core Endpoints**
- `GET /` - Health check and API info
- `GET /health` - Health status
- `GET /docs` - Interactive API documentation

### **Financial Data Endpoints**
- `GET /api/net-worth` - Current net worth
- `GET /api/portfolio/value` - Portfolio value (with simulated updates)
- `GET /api/cash-flow` - Monthly income/expense data
- `GET /api/asset-allocation` - Investment allocation
- `GET /api/transactions` - Recent transactions
- `GET /api/monte-carlo` - Portfolio projections
- `GET /api/budget` - Budget analysis
- `GET /api/summary` - Complete financial summary

## 📊 Frontend Integration

### **Option A: Separate Frontend Deployment**
Deploy the Dash frontend separately (Vercel, Netlify, etc.) and connect to your Vercel API:

```python
# In frontend/dashboard.py
API_BASE = "https://your-vercel-app.vercel.app/api"
```

### **Option B: Static Frontend**
Convert the Dash app to static files and serve alongside the API.

### **Option C: External Frontend**
Use React, Vue, or any frontend framework that consumes your Vercel API.

## 🔒 Environment Variables

Set these in your Vercel dashboard:

```
ALLOWED_ORIGINS=*
SECRET_KEY=your-production-secret-key
LOG_LEVEL=INFO
```

## 🏃‍♂️ Local Development

### **Full Application (Local)**
```bash
# Use full requirements for local development
mv requirements.txt requirements_vercel.txt
mv requirements_full.txt requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run full application
./start.sh
```

### **Vercel Simulation (Local)**
```bash
# Use Vercel requirements
mv requirements.txt requirements_full.txt
mv requirements_vercel.txt requirements.txt

# Run API only
python api.py
```

## 🧪 Testing Your Vercel Deployment

Once deployed, test these URLs:

```bash
# Health check
curl https://your-app.vercel.app/health

# API documentation
# Visit: https://your-app.vercel.app/docs

# Sample data
curl https://your-app.vercel.app/api/summary
```

## 🔄 Deployment Options Summary

| Platform | Best For | Configuration |
|----------|----------|---------------|
| **Vercel** | API-only, serverless | `main.py` + `vercel.json` |
| **Railway** | Full-stack, containers | `Dockerfile` + `railway.json` |
| **Local** | Development | `./start.sh` |

## 🐛 Vercel Troubleshooting

### **Common Issues:**

1. **Build Errors**
   - Ensure `main.py` is in root directory
   - Check `requirements.txt` has minimal dependencies

2. **Cold Start Timeouts**
   - Vercel functions have cold start delays
   - First request may be slower

3. **Memory Limits**
   - Vercel has memory constraints
   - Use minimal data processing

4. **Stateless Nature**
   - No persistent database
   - Use external database for production data

## 🔗 Next Steps

1. **Deploy to Vercel** using the guide above
2. **Test API endpoints** at your Vercel URL
3. **Create frontend** that consumes your API
4. **Add authentication** if needed
5. **Connect real database** for production use

## 📚 Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [API Documentation](https://your-app.vercel.app/docs) (after deployment)

Your financial dashboard API is now ready for Vercel deployment! 🚀