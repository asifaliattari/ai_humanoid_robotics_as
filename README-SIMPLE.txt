╔══════════════════════════════════════════════════════════════╗
║   Physical AI & Humanoid Robotics - AI-Native Textbook      ║
║                    SIMPLE SETUP GUIDE                        ║
╚══════════════════════════════════════════════════════════════╝

📖 READ THIS FIRST: START-HERE.md (detailed instructions)

═══════════════════════════════════════════════════════════════

🎯 SUPER QUICK START (3 steps):

1️⃣  GET API KEYS (10 min)
   - Qdrant: https://cloud.qdrant.io/ (free)
   - Neon: https://neon.tech/ (free)
   - OpenAI: https://platform.openai.com/ (need $10 credit)

   Save all 3 keys somewhere safe!

2️⃣  RUN SETUP (5 min)
   Double-click: setup-windows.bat

   When Notepad opens:
   - Paste your API keys
   - Save (Ctrl+S)
   - Close

3️⃣  INITIALIZE DATABASE (3 min)
   Double-click: init-database.bat

   Type Y when asked
   Wait 2-3 minutes

═══════════════════════════════════════════════════════════════

🚀 START EVERYTHING:

Option A: Start Both Servers at Once
   Double-click: START-ALL.bat

Option B: Start Separately
   Double-click: start-backend.bat (terminal 1)
   Double-click: start-frontend.bat (terminal 2)

Website opens at: http://localhost:3000

═══════════════════════════════════════════════════════════════

✅ TEST AI FEATURES:

1. Translation
   - Click language button (top of page)
   - Try: Urdu (اردو) or French (Français)

2. Chatbot
   - Click 💬 button (bottom right)
   - Ask: "What is ROS 2?"

3. Selection Q&A
   - Highlight any text
   - Ask question about it

═══════════════════════════════════════════════════════════════

📁 ALL BATCH FILES EXPLAINED:

setup-windows.bat       → Install everything (run once)
init-database.bat       → Create database & embeddings (run once)
START-ALL.bat           → Start both servers (daily use)
start-backend.bat       → Start backend only
start-frontend.bat      → Start frontend only
generate-embeddings.bat → Re-generate after content changes

═══════════════════════════════════════════════════════════════

❌ TROUBLESHOOTING:

Problem: "Python not found"
Fix: Install from https://python.org/ (check "Add to PATH")

Problem: "Node not found"
Fix: Install from https://nodejs.org/

Problem: "Database error"
Fix: Check DATABASE_URL in backend\.env

Problem: "OpenAI error"
Fix: Check OPENAI_API_KEY in backend\.env + verify credits

Problem: Setup failed on psycopg2
Fix: It's OK! The setup script handles this automatically

═══════════════════════════════════════════════════════════════

📚 MORE HELP:

START-HERE.md    → Step-by-step guide with screenshots
QUICKSTART.md    → Detailed manual setup
SETUP.md         → Complete documentation
backend/README.md → API documentation

═══════════════════════════════════════════════════════════════

💰 COSTS:

Setup (one-time):
  - Embeddings: $2-5

Monthly (1,000 users):
  - OpenAI: $20-50
  - Qdrant: Free (1GB)
  - Neon: Free (512MB)

Total: ~$25-55/month

═══════════════════════════════════════════════════════════════

🎊 WHAT YOU GET:

✅ RAG Chatbot (ask anything about the book)
✅ 5 Languages (EN/UR/FR/AR/DE with auto-translate)
✅ Personalization (adapts to your hardware/experience)
✅ Fast & Cached (smart caching saves 80% costs)
✅ Production Ready (deploy to cloud when ready)

═══════════════════════════════════════════════════════════════

That's it! Double-click setup-windows.bat to begin! 🚀

═══════════════════════════════════════════════════════════════
