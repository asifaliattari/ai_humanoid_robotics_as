# 🚀 Quick Start - Just 3 Steps!

## Step 1: Get API Keys (10 min)

Get these 3 free API keys and save them somewhere:

### 1. Qdrant (Vector Database) - FREE
1. Go to https://cloud.qdrant.io/
2. Sign up → Create Cluster → Free tier
3. Copy: **Cluster URL** and **API Key**

### 2. Neon (PostgreSQL) - FREE
1. Go to https://neon.tech/
2. Sign up → Create Project
3. Copy: **Connection String** (the full postgresql://... URL)

### 3. OpenAI (LLM) - $10 credit needed
1. Go to https://platform.openai.com/
2. Sign up → API Keys → Create Key
3. Copy: **API Key** (starts with sk-...)
4. Add $10 credit (Billing → Add payment method)

---

## Step 2: Run Setup (5 min)

**Double-click** this file:
```
setup-windows.bat
```

This will:
- ✅ Install all Python packages
- ✅ Install all Node.js packages
- ✅ Create .env file for you to edit

When Notepad opens with `.env` file:
1. Find these lines:
```env
QDRANT_URL="https://your-cluster.qdrant.io"
QDRANT_API_KEY="your_qdrant_api_key_here"
DATABASE_URL="postgresql://user:password@..."
OPENAI_API_KEY="sk-proj-..."
```

2. Replace with your actual API keys from Step 1

3. Save and close Notepad (Ctrl+S)

---

## Step 3: Initialize Database (3 min)

**Double-click** this file:
```
init-database.bat
```

This will:
- ✅ Create database tables
- ✅ Generate embeddings (costs ~$2-5, one-time)
- ✅ Upload to Qdrant

When it asks "Continue? (Y/N)", type **Y** and press Enter.

---

## Step 4: Start Everything! 🎉

**Double-click these 2 files** (in any order):

1. **start-backend.bat** - Opens backend server
2. **start-frontend.bat** - Opens your textbook website

**Keep both windows open!**

Your website will open automatically at: http://localhost:3000

---

## Test the AI Features

### 1. Test Translation
1. Go to any page (e.g., Modules → ROS 2)
2. Click a language: 🇵🇰 Urdu or 🇫🇷 French
3. Page translates in 3-5 seconds!

### 2. Test Chatbot
1. Click the **💬 chat button** (bottom right)
2. Type: "What is ROS 2?"
3. Get an AI answer with sources!

### 3. Test Selection Q&A
1. Highlight any text on the page
2. Chat widget shows "Asking about selected text"
3. Ask a question about it!

---

## Troubleshooting

### Setup failed?
- Make sure Python and Node.js are installed
- Run as Administrator (right-click → Run as administrator)
- Check internet connection

### Database init failed?
- Check your DATABASE_URL in backend/.env
- Make sure it ends with `?sslmode=require`
- Verify Neon project is active at https://neon.tech/

### Embeddings failed?
- Check OPENAI_API_KEY in backend/.env
- Verify you have $10 credit at https://platform.openai.com/usage
- Check QDRANT_URL and QDRANT_API_KEY

### Backend won't start?
- Check all API keys in backend/.env are correct
- Try running: `cd backend && venv\Scripts\activate && python -c "import fastapi"`
- Look for error messages in the terminal

### Frontend won't start?
- Delete node_modules folder
- Run setup-windows.bat again
- Check if port 3000 is already in use

---

## Daily Usage

Every time you want to work on the project:

1. **Double-click**: start-backend.bat
2. **Double-click**: start-frontend.bat
3. **Open**: http://localhost:3000

To stop: Close both terminal windows or press Ctrl+C

---

## Need More Help?

See detailed guides:
- **QUICKSTART.md** - Detailed step-by-step guide
- **SETUP.md** - Complete setup documentation
- **backend/README.md** - API documentation

---

## What You Just Built! 🎊

✅ **RAG Chatbot** - AI assistant that knows your entire textbook
✅ **5-Language Translation** - English, Urdu, French, Arabic, German
✅ **Personalized Learning** - Content adapts to your hardware & experience
✅ **Fast & Cached** - Translations cached, responses optimized
✅ **Production-Ready** - Deploy to cloud when ready

**Total Cost**: ~$2-5 setup + $20-50/month for 1,000 users

---

**Everything working? Congratulations! 🚀**

Start learning about Physical AI & Humanoid Robotics!
