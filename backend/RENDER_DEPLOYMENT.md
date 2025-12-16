# Render Deployment Guide

## Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deploy via Dashboard

1. Go to **https://render.com/**
2. Sign up/Login with **GitHub**
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repo: `asifaliattari/ai_humanoid_robotics_as`
5. Configure the service (see below)
6. Click **"Create Web Service"**

---

## Service Configuration

When creating a new Web Service on Render, use these settings:

| Setting | Value |
|---------|-------|
| **Name** | `physical-ai-book-api` |
| **Region** | Oregon (US West) or nearest |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free (or Starter for production) |

---

## Required Environment Variables

Go to your service → **"Environment"** tab → Add these variables:

### Essential (Required)

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | Neon Postgres connection URL |
| `AUTH_SECRET` | `your-32-character-secret-key` | JWT signing secret (min 32 chars) |
| `PYTHON_VERSION` | `3.11.0` | Python version |

### Production Settings

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Environment mode |
| `DEBUG` | `False` | Disable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

### CORS Configuration (Important!)

| Variable | Value |
|----------|-------|
| `CORS_ORIGINS` | `'["https://asifaliattari.github.io", "https://ai-humanoid-robotics-as.vercel.app"]'` |

### Optional (For AI Features)

| Variable | Example | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | `sk-...` | For RAG chatbot & translation |
| `QDRANT_URL` | `https://xxx.qdrant.io` | Vector database URL |
| `QDRANT_API_KEY` | `your-key` | Qdrant API key |

---

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
cd D:\hakathon\ai_humanoid_robotics_as
git add .
git commit -m "feat: add Render deployment configuration"
git push origin main
```

### Step 2: Create Neon Database (Free)

1. Go to **https://neon.tech/**
2. Sign up (free tier available)
3. Create a new project
4. Copy the connection string (looks like):
   ```
   postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

### Step 3: Deploy on Render

1. Go to **https://render.com/dashboard**
2. Click **"New +"** → **"Web Service"**
3. Connect to GitHub and select your repo
4. Set **Root Directory**: `backend`
5. Set **Build Command**: `pip install -r requirements.txt`
6. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Click **"Advanced"** → Add environment variables
8. Click **"Create Web Service"**

### Step 4: Wait for Deployment

- Render will build and deploy your app
- This takes 2-5 minutes on first deploy
- Watch the logs for any errors

### Step 5: Get Your Backend URL

After successful deployment, Render provides a URL like:
```
https://physical-ai-book-api.onrender.com
```

---

## Update Frontend to Use Render Backend

Edit `src/config/api.ts`:

```typescript
// Change this line
const PRODUCTION_BACKEND_URL = 'https://physical-ai-book-api.onrender.com';
```

Then push the frontend changes:
```bash
git add src/config/api.ts
git commit -m "feat: connect frontend to Render backend"
git push origin main
```

---

## All Environment Variables

Copy this template and fill in your values:

```env
# Required
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require
AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
PYTHON_VERSION=3.11.0

# Production Settings
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO

# CORS - Add your frontend URLs
CORS_ORIGINS='["https://asifaliattari.github.io", "https://your-app.vercel.app"]'

# Optional - AI Features
OPENAI_API_KEY=sk-your-openai-api-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=physical_ai_book

# Optional - Advanced Settings
DATABASE_POOL_SIZE=5
ACCESS_TOKEN_EXPIRE_MINUTES=30
RAG_TOP_K_RESULTS=5
```

---

## Testing Your Deployment

### Test Health Endpoint

```bash
curl https://physical-ai-book-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Physical AI Book API",
  "version": "1.0.0",
  "environment": "production"
}
```

### Test User Registration

```bash
curl -X POST https://physical-ai-book-api.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456","name":"Test User"}'
```

### Test User Login

```bash
curl -X POST https://physical-ai-book-api.onrender.com/api/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

---

## Troubleshooting

### Issue: Build fails

**Check:**
- Root directory is set to `backend`
- `requirements.txt` exists in backend folder
- Python version is supported (3.11)

**Solution:**
```bash
# Verify requirements.txt is valid
pip install -r requirements.txt --dry-run
```

### Issue: "Application failed to respond"

**Check:**
- Start command uses `$PORT` (Render provides this)
- Health check path is `/health`

**Solution:**
Ensure start command is:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Issue: Database connection error

**Check:**
- `DATABASE_URL` is correct
- SSL mode is included (`?sslmode=require`)
- Neon database is active (not suspended)

### Issue: CORS errors in browser

**Check:**
- Frontend URL is in `CORS_ORIGINS`
- JSON format is correct (with quotes)

**Solution:**
```
CORS_ORIGINS='["https://your-frontend.com"]'
```

### Issue: Auth not working

**Check:**
- `AUTH_SECRET` is at least 32 characters
- Same secret across all deployments

---

## Render Free Tier Limitations

| Limit | Value |
|-------|-------|
| **Sleep after inactivity** | 15 minutes |
| **Monthly hours** | 750 hours |
| **RAM** | 512 MB |
| **CPU** | Shared |

**Note:** Free tier services "spin down" after 15 minutes of inactivity. First request after sleep takes ~30 seconds.

**Upgrade to Starter ($7/month)** for:
- No sleep
- Persistent disk
- Better performance

---

## Files for Render Deployment

| File | Purpose |
|------|---------|
| `render.yaml` | Render blueprint configuration |
| `build.sh` | Custom build script (optional) |
| `Dockerfile` | Container configuration |
| `requirements.txt` | Python dependencies |

---

## Generate AUTH_SECRET

Run this command to generate a secure secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use:
```bash
openssl rand -base64 32
```

---

## Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Neon database created
- [ ] Render service created
- [ ] Root directory set to `backend`
- [ ] Environment variables added:
  - [ ] `DATABASE_URL`
  - [ ] `AUTH_SECRET`
  - [ ] `CORS_ORIGINS`
  - [ ] `ENVIRONMENT=production`
  - [ ] `DEBUG=False`
- [ ] Deployment successful
- [ ] Health endpoint responds
- [ ] Frontend updated with backend URL
