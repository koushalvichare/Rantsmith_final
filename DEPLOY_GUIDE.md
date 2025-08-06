# 🚀 RantSmith AI - Complete Deployment Guide

## ✅ Your Project is Ready for Deployment!

### 📋 What's Been Configured:
- ✅ `render.yaml` - Complete Render configuration with your API keys
- ✅ `frontend/vercel.json` - Vercel configuration for frontend
- ✅ `Procfile` - Alternative Render deployment method
- ✅ All environment variables pre-configured

---

## 🌐 Deploy Backend to Render

### Method 1: One-Click Deploy (Recommended)
1. **Go to**: [render.com](https://render.com)
2. **New Web Service** → **Connect GitHub** → Select `koushalvichare/RantSmith`
3. **Render will automatically use `render.yaml`** - just click **"Create Web Service"**
4. ✅ **Done!** Your API keys and settings are already configured

### Method 2: Manual Setup (If Method 1 fails)
1. **Go to**: [render.com](https://render.com)
2. **New Web Service** → **Connect GitHub** → Select `koushalvichare/RantSmith`
3. **Manual Settings**:
   - **Name**: `rantsmith-backend`
   - **Build Command**: `pip install --upgrade pip && pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2 Flask-CORS==4.0.0 Werkzeug==2.3.7 python-dotenv==1.0.0 PyJWT==2.8.0 gunicorn==21.2.0 google-generativeai==0.8.5 requests==2.31.0 SQLAlchemy==2.0.20 Pillow==10.0.0 bcrypt==4.0.1`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT run:app`

4. **Environment Variables**:
   ```
   FLASK_ENV=production
   DEBUG=false
   SECRET_KEY=(auto-generated)
   GEMINI_API_KEY=AIzaSyBzhRTPareqAhVlqGfvlHjn57dA_ei2sTE
   ELEVENLABS_API_KEY=sk_03dd9427c42b5ac7818b16d82278c60554ae8c14aad586a4
   RUNWAYML_API_KEY=key_645fe4a90f0523aa467a120611d7dc2c1063093414e7be0d3055d350601d4fe56b48c133438dac13b40ee4870a9c4dcebfbe42116aaeb21b0f944502d8b05bf9
   ```

---

## 🎨 Deploy Frontend to Vercel

### One-Click Deploy:
1. **Go to**: [vercel.com](https://vercel.com)
2. **New Project** → **Import** → Select `koushalvichare/RantSmith`
3. **Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
4. **Deploy** - Vercel will use `frontend/vercel.json` automatically!

### After Deployment:
- Your frontend will automatically connect to: `https://rantsmith-backend.onrender.com`
- Update this URL in Vercel if your Render app has a different name

---

## 🔗 Final Steps

### 1. Get Your URLs:
- **Backend**: `https://rantsmith-backend.onrender.com`
- **Frontend**: `https://your-project-name.vercel.app`

### 2. Test Your Deployment:
- Visit your frontend URL
- Try the AI chat with Dr. Sarah psychologist
- Test: "Tell me a psychology joke" - should get creative, non-repeated responses

### 3. Update CORS (if needed):
If you get CORS errors, add your Vercel domain to the backend CORS settings.

---

## 🎯 Key Features Ready:
- ✅ **Psychologist AI Personality** - Dr. Sarah with mood-uplifting responses
- ✅ **Creative Joke Generation** - No more repeated jokes
- ✅ **Emotional Support** - Professional psychological guidance
- ✅ **All API Keys Pre-configured**

---

## 🆘 Troubleshooting

### If Render Build Fails:
- The `render.yaml` bypasses `requirements.txt` wheel issues
- Uses manual package installation
- All essential packages included

### If Frontend API Calls Fail:
- Check that backend URL in `frontend/vercel.json` matches your actual Render URL
- Update environment variable in Vercel dashboard if needed

---

## 🎉 You're Ready to Deploy!

Your psychologist AI app with mood-uplifting responses and creative joke generation is ready for production! 🧠✨

**Repository**: https://github.com/koushalvichare/RantSmith
**Status**: ✅ Production Ready
