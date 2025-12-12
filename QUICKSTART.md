# Quick Start Guide - Step by Step

Follow these exact steps to get your AI-native textbook running in 15 minutes.

---

## Step 1: Get API Keys (10 minutes)

You need 3 free API keys. Follow each section carefully.

### 1.1 Get Qdrant API Key (Vector Database)

**What it's for**: Stores embeddings for the RAG chatbot to search your book content.

1. Go to https://cloud.qdrant.io/
2. Click **"Sign Up"** (top right)
3. Sign up with Google or Email
4. After login, click **"Create Cluster"**
5. Fill in:
   - **Cluster name**: `physical-ai-book`
   - **Region**: Choose closest to you (e.g., `us-east-1`)
   - **Plan**: Select **"Free"** (1GB storage)
6. Click **"Create"**
7. Wait 1-2 minutes for cluster to provision
8. Once ready, you'll see your cluster in the dashboard
9. Click on your cluster name
10. **Copy these 2 values**:
    - **Cluster URL**: Something like `https://abc123-xyz.qdrant.tech`
    - **API Key**: Click "API Keys" tab → "Create Key" → Copy the key (starts with `qdr-...`)

**Save these values** - you'll need them in Step 2.

---

### 1.2 Get Neon Postgres URL (Database)

**What it's for**: Stores user profiles, reading progress, translation cache.

1. Go to https://neon.tech/
2. Click **"Sign Up"** (top right)
3. Sign up with Google or GitHub
4. After login, click **"Create a project"**
5. Fill in:
   - **Project name**: `physical-ai-book`
   - **Region**: Choose closest to you
   - **Postgres version**: 16 (default)
6. Click **"Create project"**
7. You'll see a "Connection Details" popup
8. **Copy the connection string**:
   - Click **"Pooled connection"** tab
   - Copy the entire string (looks like):
     ```
     postgresql://user:password@ep-abc123.us-east-2.aws.neon.tech/neondb?sslmode=require
     ```
   - **IMPORTANT**: This string contains your password - keep it secret!

**Save this value** - you'll need it in Step 2.

---

### 1.3 Get OpenAI API Key (LLM & Embeddings)

**What it's for**: Powers translations, chatbot answers, and embeddings.

1. Go to https://platform.openai.com/
2. Click **"Sign Up"** or **"Log In"**
3. After login, click your profile icon (top right)
4. Click **"API Keys"**
5. Click **"Create new secret key"**
6. Give it a name: `physical-ai-book`
7. **Copy the key immediately** (starts with `sk-...`)
   - ⚠️ **WARNING**: You can only see this once! Copy it now.

**Add Credits** (required):
1. Click **"Billing"** (left sidebar)
2. Click **"Add payment method"**
3. Add credit card
4. Click **"Add credits"** → Add **$10** (will last 2-3 months)

**Save this value** - you'll need it in Step 2.

---

## Step 2: Configure Backend (2 minutes)

Now you'll put those API keys into the configuration file.

### 2.1 Open the .env file

```bash
# Navigate to backend directory
cd D:\hakathon\ai_humanoid_robotics_as\backend

# Copy the example file
copy .env.example .env

# Open .env in Notepad
notepad .env
```

### 2.2 Fill in your API keys

Replace the placeholder values with your actual keys:

**BEFORE** (what you'll see):
```env
QDRANT_URL=https://your-cluster-id.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=physical-ai-book

DATABASE_URL=postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

OPENAI_API_KEY=sk-your-openai-api-key-here
```

**AFTER** (example with your real values):
```env
QDRANT_URL=https://abc123-xyz.qdrant.tech
QDRANT_API_KEY=qdr-1234567890abcdef
QDRANT_COLLECTION_NAME=physical-ai-book

DATABASE_URL=postgresql://neondb_owner:npg_abc123@ep-cool-bonus-123.us-east-2.aws.neon.tech/neondb?sslmode=require

OPENAI_API_KEY=sk-proj-abcdef1234567890
```

**Save the file**: `Ctrl+S` → Close Notepad

---

## Step 3: Install Dependencies (3 minutes)

You need Python and Node.js installed first.

### 3.1 Check if you have Python

```bash
python --version
```

**If you see**: `Python 3.11.x` or higher → ✅ You're good!

**If you see an error**:
1. Download Python: https://www.python.org/downloads/
2. Install (check "Add Python to PATH")
3. Restart terminal and try again

### 3.2 Check if you have Node.js

```bash
node --version
```

**If you see**: `v18.x` or higher → ✅ You're good!

**If you see an error**:
1. Download Node.js: https://nodejs.org/
2. Install the LTS version
3. Restart terminal and try again

### 3.3 Install Backend Dependencies

```bash
# Make sure you're in backend directory
cd D:\hakathon\ai_humanoid_robotics_as\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies (takes 1-2 minutes)
pip install -r requirements.txt
```

**You should see**: Lots of packages installing. This is normal!

### 3.4 Install Frontend Dependencies

```bash
# Go to project root
cd D:\hakathon\ai_humanoid_robotics_as

# Install Node packages (takes 2-3 minutes)
npm install
```

**You should see**: Progress bar installing packages. This is normal!

---

## Step 4: Initialize Database (1 minute)

Create the database tables.

```bash
# Make sure you're in backend directory
cd D:\hakathon\ai_humanoid_robotics_as\backend

# Activate virtual environment if not already active
venv\Scripts\activate

# Run database migrations
alembic upgrade head
```

**You should see**:
```
INFO  [alembic.runtime.migration] Running upgrade -> 001, Initial schema
```

✅ **Success!** Database tables created.

---

## Step 5: Generate Embeddings (2-3 minutes)

This creates searchable embeddings of your book content for the RAG chatbot.

```bash
# Make sure you're in backend directory and venv is activated
cd D:\hakathon\ai_humanoid_robotics_as\backend
venv\Scripts\activate

# Run embedding generation script
python -m scripts.generate_embeddings
```

**You should see**:
```
INFO - Found 10 markdown files
INFO - Processed foundations/index.md: 3 sections → 5 chunks
INFO - Processed modules/ros2/index.md: 15 sections → 23 chunks
...
INFO - Total chunks: 234
INFO - Generating embeddings...
INFO - Generated 234 embeddings
INFO - Uploading to Qdrant...
INFO - Successfully uploaded 234 chunks to Qdrant
INFO - Test search for 'What is ROS 2?' returned 3 results
✅ Embedding generation complete
```

**Cost**: This will use about $2-5 of your OpenAI credits (one-time cost).

**Time**: Takes 2-3 minutes depending on internet speed.

✅ **Success!** Your book is now searchable.

---

## Step 6: Start Backend Server (30 seconds)

```bash
# Make sure you're in backend directory and venv is activated
cd D:\hakathon\ai_humanoid_robotics_as\backend
venv\Scripts\activate

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**You should see**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Backend is running!**

**Test it**: Open http://localhost:8000/docs in your browser.

You should see the **Swagger API documentation** with all endpoints listed.

**Leave this terminal running** - don't close it!

---

## Step 7: Start Frontend (30 seconds)

Open a **NEW terminal** (keep backend running).

```bash
# Go to project root
cd D:\hakathon\ai_humanoid_robotics_as

# Start Docusaurus development server
npm start
```

**You should see**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

Your browser should automatically open to http://localhost:3000

✅ **Frontend is running!**

---

## Step 8: Test Everything Works! 🎉

### 8.1 Test the Website

1. Your browser should show the homepage
2. Click **"Modules"** → **"Module 1: ROS 2"**
3. You should see the ROS 2 content

### 8.2 Test Translation

1. Scroll to top of any page
2. You should see language buttons: 🇬🇧 English | 🇵🇰 Urdu | 🇫🇷 French | 🇸🇦 Arabic | 🇩🇪 German
3. Click **"Urdu"**
4. Wait 3-5 seconds (first time)
5. Page should translate to Urdu with right-to-left layout
6. Click **"English"** to return to original

✅ **Translation works!**

### 8.3 Test Personalization

1. Click the **"Personalize for Me"** button (near language toggle)
2. If not signed in, you'll see: "Please sign in to personalize content"
3. For now, sign-in is optional - we'll add it later

### 8.4 Test RAG Chatbot

1. Look for the **floating chat button** (bottom right): 💬
2. Click it
3. The chat widget opens
4. Type: **"What is ROS 2?"**
5. Press Enter
6. Wait 2-3 seconds
7. You should get an answer with sources cited!

✅ **RAG Chatbot works!**

Example answer:
```
ROS 2 (Robot Operating System 2) is the communication framework
that serves as the "nervous system" for humanoid robots. It enables
independent software components (nodes) to exchange messages,
coordinate actions, and share sensor data in real-time.

Sources:
- modules/ros2/index
- foundations/index
```

---

## Step 9: Try Selection-Based Q&A

1. On any page, **highlight some text** with your mouse
2. The chat widget should show: "✂️ Asking about selected text"
3. Type a question about that text, like: **"Explain this in simpler terms"**
4. Get an answer focused on your selected text!

✅ **Selection-based Q&A works!**

---

## Troubleshooting

### "Connection to Qdrant failed"

**Fix**:
1. Check your `backend/.env` file
2. Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
3. Go to https://cloud.qdrant.io/ and verify cluster is running
4. Restart backend: `Ctrl+C` → `uvicorn main:app --reload`

### "Database connection error"

**Fix**:
1. Check your `backend/.env` file
2. Verify `DATABASE_URL` is correct (including `?sslmode=require` at end)
3. Go to https://neon.tech/ and verify project is active
4. Restart backend

### "OpenAI API rate limit exceeded"

**Fix**:
1. Go to https://platform.openai.com/settings/organization/billing
2. Verify you have credits
3. Add more credits if needed
4. Wait 1 minute and try again

### "Translation not working"

**Check**:
1. Backend is running (http://localhost:8000/docs should work)
2. Open browser console (F12) and check for errors
3. Verify OpenAI API key is valid
4. Check backend terminal for error messages

### "Chatbot not responding"

**Check**:
1. Backend is running
2. Embeddings were generated (Step 5 completed successfully)
3. Open browser console (F12) for errors
4. Try asking a simple question: "What is Physical AI?"

### "Port 8000 already in use"

**Fix**:
```bash
# Use different port
uvicorn main:app --reload --port 8001

# Update frontend to use new port (in component files)
```

### "Port 3000 already in use"

**Fix**:
```bash
# Use different port
npm start -- --port 3001
```

---

## What's Running?

When everything is set up, you should have:

**Terminal 1**: Backend server
```
✅ http://localhost:8000 (FastAPI)
✅ http://localhost:8000/docs (API documentation)
```

**Terminal 2**: Frontend server
```
✅ http://localhost:3000 (Docusaurus website)
```

**Services Used**:
- ✅ Qdrant Cloud (vector database)
- ✅ Neon Postgres (user database)
- ✅ OpenAI API (translations & chatbot)

---

## Daily Usage

When you want to work on the project:

**Start Backend**:
```bash
cd D:\hakathon\ai_humanoid_robotics_as\backend
venv\Scripts\activate
uvicorn main:app --reload
```

**Start Frontend** (new terminal):
```bash
cd D:\hakathon\ai_humanoid_robotics_as
npm start
```

**Stop Everything**:
- Press `Ctrl+C` in both terminals

---

## Cost Tracking

Monitor your OpenAI usage:
1. Go to https://platform.openai.com/usage
2. Check daily usage
3. Set up alerts if needed

**Expected costs**:
- Embeddings (one-time): $2-5
- Translations: ~$0.05 each (80% cached after first request)
- Chatbot: ~$0.01-0.03 per query
- **Monthly estimate**: $20-50 for 1,000 users

---

## Next Steps

✅ Everything working? Great!

Now you can:
1. **Explore the book**: Navigate through all modules
2. **Try all AI features**: Translation, personalization, chatbot
3. **Add more content**: Edit files in `docs/` directory
4. **Regenerate embeddings**: Run Step 5 again after content changes
5. **Deploy to production**: See [SETUP.md](SETUP.md) for deployment guide

---

## Getting Help

If you get stuck:

1. **Check this guide** - Most issues are covered in Troubleshooting
2. **Check terminal output** - Error messages usually explain the problem
3. **Check browser console** (F12) - Frontend errors show here
4. **Verify API keys** - 90% of issues are incorrect API keys
5. **Read detailed docs**: [SETUP.md](SETUP.md)

---

**Congratulations! 🎉**

Your AI-native textbook is now running with:
- ✅ RAG chatbot (ask anything about the book)
- ✅ Multi-language translation (5 languages)
- ✅ Personalized learning (adapts to your setup)

Start exploring and learning about Physical AI & Humanoid Robotics! 🤖
