#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI backend..."
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for the backend to start
sleep 5

# Start the Dash frontend
echo "Starting Dash frontend..."
cd /app/frontend && python dashboard.py