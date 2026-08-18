# ⟨ CodeAnalyzer /⟩ — AI-Powered Code Review

A full-stack web application that analyzes your code using **Google Gemini AI**, detects bugs,
corrects errors, optimizes performance, and stores everything in a database.

**Stack:** Python + FastAPI + SQLAlchemy + SQLite + Gemini AI + Vanilla HTML/JS Frontend

---

## 📁 Project Structure

```
code-analyzer/
├── backend/
│   ├── main.py                  ← FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── db/
│   │   └── database.py          ← SQLAlchemy engine + session
│   ├── models/
│   │   └── analysis.py          ← DB table definitions
│   ├── schemas/
│   │   └── analysis.py          ← Pydantic request/response models
│   ├── services/
│   │   └── gemini_service.py    ← Gemini AI + static analysis
│   └── routers/
│       ├── home.py              ← /api/stats
│       ├── analyze.py           ← /api/analyze/
│       └── history.py           ← /api/history/
└── frontend/
    └── index.html               ← Complete 3-page SPA (Home, Analyze, History)
```

---

## 🔌 How Everything Connects

```
Browser (index.html)
        │  fetch() HTTP requests
        ▼
FastAPI Backend (port 8000)
        │  SQLAlchemy ORM
        ▼
SQLite Database (code_analyzer.db)

FastAPI Backend
        │  google-generativeai SDK
        ▼
Google Gemini API (cloud)
```

---

## 🚀 Setup on Your Laptop (Step by Step)

### Step 1 — Install Python
Make sure you have Python 3.10+ installed:
```bash
python --version   # Should show 3.10 or higher
```
Download from https://www.python.org/downloads/ if needed.

### Step 2 — Clone/Create the project folder
```bash
mkdir code-analyzer
cd code-analyzer
```

### Step 3 — Set up Python virtual environment
```bash
# Create venv
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 5 — Configure environment variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key:
# Get your free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_actual_key_here
```

### Step 6 — Start the backend
```bash
# From the backend/ directory:
uvicorn main:app --reload --port 8000
```
You should see:
```
✅ Database tables created / verified.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 7 — Open the frontend
Open `frontend/index.html` directly in your browser — no server needed!
```
Double-click frontend/index.html
OR
# In browser: File → Open File → index.html
```

### Step 8 — Test it!
1. Go to **Analyze** tab
2. Paste some Python code (or use the example)
3. Click **Analyze →**
4. See errors, corrected code, and AI suggestions!

---

## 🔗 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Home page dashboard stats |
| POST | `/api/analyze/` | Submit code for analysis |
| GET | `/api/analyze/{id}` | Get analysis result by ID |
| DELETE | `/api/analyze/{id}` | Delete an analysis |
| GET | `/api/history/` | Paginated history list |
| GET | `/api/history/stats` | History summary statistics |
| DELETE | `/api/history/` | Clear all history |

Interactive docs available at: http://localhost:8000/docs

---

## 🗄️ Database

**Development (default):** SQLite — file created automatically as `code_analyzer.db`

**Production (PostgreSQL):** Change `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/code_analyzer
```
And install: `pip install psycopg2-binary`

**To inspect the database:**
```bash
# Install DB browser: https://sqlitebrowser.org/
# Or use Python:
python3 -c "
import sqlite3
conn = sqlite3.connect('code_analyzer.db')
cursor = conn.execute('SELECT id, title, language, error_count, status FROM analysis_records')
for row in cursor: print(row)
conn.close()
"
```

---

## 📤 Push to GitHub

### Step 1 — Create `.gitignore`
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
venv/
*.egg-info/

# Environment
.env
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db
EOF
```

### Step 2 — Initialize Git
```bash
# From the code-analyzer/ root folder:
git init
git add .
git commit -m "feat: initial commit - Code Analyzer with FastAPI + Gemini AI"
```

### Step 3 — Create GitHub repo
1. Go to https://github.com/new
2. Name it `code-analyzer`
3. Make it Public or Private
4. Do NOT initialize with README (we already have one)
5. Click **Create repository**

### Step 4 — Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/code-analyzer.git
git branch -M main
git push -u origin main
```

---

## 🌐 Deployment

### Option A — Railway (Easiest, Free Tier)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click **New Project → Deploy from GitHub repo**
4. Select `code-analyzer`
5. Set environment variables in Railway dashboard:
   - `GEMINI_API_KEY` = your key
   - `DATABASE_URL` = Railway provides PostgreSQL automatically
6. Railway auto-detects FastAPI and deploys!

### Option B — Render (Free)
1. Go to https://render.com
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Settings:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

### Option C — Self-hosted (VPS like DigitalOcean/Hostinger)
```bash
# On your server:
git clone https://github.com/YOUR_USERNAME/code-analyzer.git
cd code-analyzer/backend
pip install -r requirements.txt
cp .env.example .env && nano .env  # add your keys

# Run with gunicorn (production ASGI):
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment
For the frontend `index.html`, deploy to:
- **Netlify**: Drag & drop the `frontend/` folder at netlify.com
- **GitHub Pages**: Enable in repo Settings → Pages

**Important:** Update the `API` constant in `index.html` to your deployed backend URL:
```javascript
const API = 'https://your-backend.railway.app/api';  // Change this!
```

---

## 🔑 Getting Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click **Create API Key**
4. Copy it to your `.env` file

**Free tier:** 15 requests/minute, 1 million tokens/day — more than enough for development!

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in venv |
| CORS error in browser | Make sure FastAPI is running on port 8000 |
| Gemini returns `None` | Check GEMINI_API_KEY in .env |
| DB not created | uvicorn creates it on first start |
| Port 8000 in use | `uvicorn main:app --port 8001` |
