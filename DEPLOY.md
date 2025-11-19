# Deployment Guide

## Prerequisites

- GitHub Account
- Vercel Account (for Frontend)
- Render or Railway Account (for Backend)
- Google Gemini API Key

## Backend Deployment (Render)

1. **Create a new Web Service** on Render.
2. **Connect your GitHub repository**.
3. **Settings**:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `GOOGLE_API_KEY`: Your Gemini API key.
   - `PYTHON_VERSION`: `3.11.0`

## Frontend Deployment (Vercel)

1. **Import Project** on Vercel.
2. **Select the `frontend` directory** as the root.
3. **Build Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL`: The URL of your deployed backend (e.g., `https://cv-sob-medida-backend.onrender.com`).

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs tests on every push to `main`.
Deployments are handled automatically by Vercel and Render when changes are pushed to the connected branch.
