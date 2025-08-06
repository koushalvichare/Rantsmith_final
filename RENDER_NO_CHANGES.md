# 🚀 Deploy to Render WITHOUT Changing Your Project

## Keep Your Project Unchanged - Configure in Render Dashboard Only

### Step 1: Go to Render.com
1. Sign up/login at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `koushalvichare/RantSmith`

### Step 2: Configure in Render Dashboard
**DON'T use any config files - set everything manually:**

#### Basic Settings:
- **Name**: `rantsmith-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install --upgrade pip && pip install Flask Flask-SQLAlchemy Flask-Login Flask-CORS gunicorn google-generativeai requests python-dotenv PyJWT SQLAlchemy Pillow bcrypt Werkzeug`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT run:app`
- **Python Version**: Leave default (3.11)

#### Environment Variables (Add these in Dashboard):
```
FLASK_ENV=production
DEBUG=false
SECRET_KEY=your-auto-generated-secret-key
GEMINI_API_KEY=AIzaSyBzhRTPareqAhVlqGfvlHjn57dA_ei2sTE
GOOGLE_API_KEY=AIzaSyBzhRTPareqAhVlqGfvlHjn57dA_ei2sTE
ELEVENLABS_API_KEY=sk_03dd9427c42b5ac7818b16d82278c60554ae8c14aad586a4
RUNWAYML_API_KEY=key_645fe4a90f0523aa467a120611d7dc2c1063093414e7be0d3055d350601d4fe56b48c133438dac13b40ee4870a9c4dcebfbe42116aaeb21b0f944502d8b05bf9
DATABASE_URL=sqlite:///rantsmith.db
```

### Step 3: Deploy
Click "Create Web Service" and let it deploy!

## Why This Works:
- ✅ No changes to your project files
- ✅ Bypasses the requirements.txt wheel build issue
- ✅ Installs only essential packages manually
- ✅ Your code stays exactly as it is

## Alternative Build Commands (if first one fails):

### Option 1 - Basic Packages:
```bash
pip install --upgrade pip && pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-CORS==4.0.0 gunicorn==21.2.0 google-generativeai==0.8.5 requests==2.31.0 python-dotenv==1.0.0
```

### Option 2 - Even More Minimal:
```bash
pip install Flask gunicorn google-generativeai requests python-dotenv
```

## Frontend Deployment (After Backend Works):
1. Go to [vercel.com](https://vercel.com)
2. Import your repo
3. Set root directory to `frontend`
4. Add environment variable: `VITE_API_BASE_URL=https://your-render-url.onrender.com`

## 🎯 Key Points:
- **Your GitHub repo stays unchanged**
- **No modifications to your project**
- **Everything configured in Render dashboard**
- **Your psychologist AI will work perfectly**

This approach keeps your project pristine while making it deployable! 🚀
