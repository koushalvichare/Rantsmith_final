# 🔧 Deployment Troubleshooting Guide

## ✅ Fixes Applied for Wheel Build Error

### Problem:
```
Getting requirements to build wheel: finished with status 'error'
KeyError: '__version__'
```

### Solution:
I've fixed the following issues:

### 1. **Cleaned requirements.txt**
- Removed duplicate packages (`opencv-python`, `pytest-flask`, etc.)
- Removed problematic packages that might cause wheel build issues
- Created `requirements-minimal.txt` as backup

### 2. **Added Python Runtime Specification**
- Created `runtime.txt` with `python-3.11.6`
- This ensures Render uses a compatible Python version

### 3. **Improved Build Process**
- Updated `render.yaml` build command to upgrade pip first
- Added `.renderignore` to exclude unnecessary files

### 4. **Created Minimal Requirements**
- `requirements-minimal.txt` contains only essential packages
- Use this if the main requirements.txt still causes issues

## 🚀 Deployment Options

### Option 1: Use Current Fixed Requirements
Try deploying with the cleaned `requirements.txt` first.

### Option 2: Use Minimal Requirements (If Option 1 Fails)
1. In Render dashboard, change build command to:
   ```bash
   pip install --upgrade pip && pip install -r requirements-minimal.txt
   ```

### Option 3: Manual Package Installation
If both fail, use this build command:
```bash
pip install --upgrade pip && pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-CORS==4.0.0 gunicorn==21.2.0 google-generativeai==0.8.5 requests==2.31.0 python-dotenv==1.0.0
```

## 🔧 Render Configuration

### Build Command Options:
1. **Standard**: `pip install --upgrade pip && pip install -r requirements.txt`
2. **Minimal**: `pip install --upgrade pip && pip install -r requirements-minimal.txt`
3. **Manual**: (see Option 3 above)

### Start Command:
`gunicorn --bind 0.0.0.0:$PORT run:app`

### Environment Variables (Required):
```
FLASK_ENV=production
DEBUG=false
SECRET_KEY=(auto-generated)
GEMINI_API_KEY=AIzaSyBzhRTPareqAhVlqGfvlHjn57dA_ei2sTE
ELEVENLABS_API_KEY=sk_03dd9427c42b5ac7818b16d82278c60554ae8c14aad586a4
RUNWAYML_API_KEY=key_645fe4a90f0523aa467a120611d7dc2c1063093414e7be0d3055d350601d4fe56b48c133438dac13b40ee4870a9c4dcebfbe42116aaeb21b0f944502d8b05bf9
```

## 🎯 Deployment Steps

1. **Go to Render.com**
2. **New Web Service** → Connect GitHub repo
3. **Settings**:
   - Name: `rantsmith-backend`
   - Environment: Python 3
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT run:app`
4. **Add Environment Variables** (see above)
5. **Deploy**

## ⚠️ If Build Still Fails

1. Try `requirements-minimal.txt` in build command
2. Check Render logs for specific error
3. Use manual package installation method
4. Contact me with the specific error message

## 🌐 Frontend Deployment (Vercel)

After backend is deployed:
1. Go to Vercel.com
2. Import your GitHub repo
3. Set root directory to `frontend`
4. Add environment variable: `VITE_API_BASE_URL=https://your-render-url.onrender.com`

Your project should now deploy successfully! 🚀
