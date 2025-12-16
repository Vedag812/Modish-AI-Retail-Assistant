# 🚀 Deployment Guide - Retail Sales Agent

This guide will help you deploy the Retail Sales Agent application to the cloud.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Next.js App    │────▶│  FastAPI Server │────▶│    Firebase     │
│   (Vercel)      │     │  (Render/Rail)  │     │   Firestore     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Frontend              Backend               Database
```

---

## Step 1: Deploy Backend (FastAPI) to Render

### 1.1 Create Render Account
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub account

### 1.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Vedag812/Retail-Agent`
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `retail-sales-api` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | *(leave empty)* |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api_server:app --host 0.0.0.0 --port $PORT` |

### 1.3 Set Environment Variables
In Render dashboard, go to **"Environment"** tab and add:

| Variable | Value |
|----------|-------|
| `GEMINI_API_KEY` | `AIzaSyDYgkvI5bp4DY6uy12GJRTBqSpzjf1-WFE` |
| `RAZORPAY_KEY_ID` | `rzp_test_RnUJfj8QOYSc6i` |
| `RAZORPAY_KEY_SECRET` | `Zez8aIEtQj7rzVeYPd7ljLoo` |
| `DEFAULT_MODEL` | `gemini-2.5-flash` |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | *(See step 1.4)* |

### 1.4 Firebase Service Account JSON
Copy the **entire content** of your `firebase-service-account.json` file and paste it as the value for `FIREBASE_SERVICE_ACCOUNT_JSON`.

**Important:** Make sure it's a single line or properly escaped JSON string.

You can convert it using this PowerShell command:
```powershell
(Get-Content firebase-service-account.json -Raw) -replace "`r`n", "" -replace "`n", ""
```

### 1.5 Deploy
Click **"Create Web Service"** and wait for deployment (3-5 minutes).

Your backend URL will be something like: `https://retail-sales-api.onrender.com`

---

## Step 2: Deploy Frontend (Next.js) to Vercel

### 2.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Authorize access to your repositories

### 2.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Select your repository: `Vedag812/Retail-Agent`
3. Configure:

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Next.js` |
| **Root Directory** | `ey-frontend/E-Y` |
| **Build Command** | `npm run build` |
| **Output Directory** | `.next` |
| **Install Command** | `npm install` |

### 2.3 Set Environment Variables
Add these environment variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://retail-sales-api.onrender.com` *(your Render URL)* |
| `GOOGLE_GENAI_API_KEY` | `AIzaSyDYgkvI5bp4DY6uy12GJRTBqSpzjf1-WFE` |

### 2.4 Deploy
Click **"Deploy"** and wait (2-3 minutes).

Your frontend URL will be: `https://your-project.vercel.app`

---

## Step 3: Post-Deployment Configuration

### 3.1 Update CORS (Optional)
If you want to restrict CORS to only your Vercel domain, add this environment variable in Render:

| Variable | Value |
|----------|-------|
| `ALLOWED_ORIGINS` | `https://your-project.vercel.app` |

### 3.2 Firebase Security Rules
Ensure your Firestore rules allow access from your deployed backend.

### 3.3 Test the Deployment
1. Open your Vercel URL
2. Try logging in
3. Chat with the AI assistant
4. Add products to cart
5. Test checkout flow

---

## Alternative: Deploy Backend to Railway

### Railway Setup
1. Go to [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Select your repository
4. Add environment variables (same as Render)
5. Railway auto-detects `Procfile` and deploys

---

## Environment Variables Summary

### Backend (Render/Railway)
```env
GEMINI_API_KEY=your_gemini_key
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=xxx
DEFAULT_MODEL=gemini-2.5-flash
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
GOOGLE_GENAI_API_KEY=your_gemini_key
```

---

## Troubleshooting

### Backend not starting?
- Check logs in Render dashboard
- Ensure all environment variables are set
- Verify `FIREBASE_SERVICE_ACCOUNT_JSON` is valid JSON

### CORS errors?
- Backend allows all origins by default (`*`)
- Check browser console for specific errors

### Firebase connection issues?
- Verify service account JSON is correctly formatted
- Check Firebase project settings

### Chatbot not responding?
- Check backend logs for Gemini API errors
- Verify `GEMINI_API_KEY` is valid

---

## Costs

| Service | Free Tier |
|---------|-----------|
| **Vercel** | 100GB bandwidth, unlimited deployments |
| **Render** | 750 hours/month (spins down after 15min inactivity) |
| **Railway** | $5 free credits/month |
| **Firebase** | 1GB storage, 50K reads/day, 20K writes/day |

---

## Quick Deploy Commands

After any code changes:
```powershell
# Commit and push
git add -A
git commit -m "Your changes"
git push origin main

# Both Vercel and Render will auto-deploy on push!
```

---

## Support

Need help? Check the main [README.md](README.md) or open an issue on GitHub.
