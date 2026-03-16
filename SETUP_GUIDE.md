# FarmSphere - Complete Setup & Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [API Keys Configuration](#api-keys-configuration)
3. [Running Locally](#running-locally)
4. [Deployment to Render](#deployment-to-render)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### System Requirements
- **OS:** Windows, macOS, or Linux
- **Python:** 3.9 or higher
- **Memory:** 2GB RAM minimum
- **Storage:** 500MB available

### Step 1: Install Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

### Step 2: Download FarmSphere

Option A: Using Git
```bash
git clone https://github.com/yourusername/FarmSphere.git
cd FarmSphere
```

Option B: Download ZIP
1. Extract the ZIP file
2. Open terminal in extracted folder

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Requests (API calls)
- Pillow (image processing)
- NumPy (numerical computing)
- Scikit-learn (machine learning)
- Google Generative AI (chatbot)
- Gunicorn (production server)

---

## API Keys Configuration

### 1. Get Gemini API Key

1. Visit https://makersuite.google.com/
2. Click "Get API Key" button
3. Click "Create API Key"
4. Select or create project
5. Copy the API key

### 2. Get OpenWeatherMap API Key

1. Visit https://openweathermap.org/api
2. Click "Sign Up" or "Sign In"
3. Create free account
4. Go to "API Keys" section
5. Copy Default Key

### 3. Setup .env File

```bash
# Copy example file
cp .env.example .env

# Edit .env with your keys
```

**Windows (Notepad):**
```
Right-click .env → Edit → Paste your keys
```

**macOS/Linux (Terminal):**
```bash
nano .env
# Paste:
GEMINI_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
SECRET_KEY=your_secret_here
FLASK_ENV=development
```

---

## Running Locally

### Start the Server

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### Access the App

Open in browser: **http://localhost:5000**

### Pages Available

- **Home:** http://localhost:5000/
- **Dashboard:** http://localhost:5000/dashboard
- **Disease Diagnosis:** http://localhost:5000/disease-diagnosis
- **Weather:** http://localhost:5000/weather
- **Price Prediction:** http://localhost:5000/price-prediction
- **Chatbot:** http://localhost:5000/chatbot

### Stop the Server

Press `Ctrl+C` in terminal

---

## Deployment to Render

### Prerequisites

- GitHub account
- Render account (free at https://render.com)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "FarmSphere - Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/FarmSphere.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Click "Sign Up"
3. Connect with GitHub
4. Authorize Render

### Step 3: Deploy Application

1. Go to https://dashboard.render.com
2. Click "New +" button
3. Select "Web Service"
4. Connect GitHub repository
5. Select FarmSphere repo

### Step 4: Configure Service

**Basic Settings:**
- **Name:** farmsphere (or your choice)
- **Environment:** Python 3.11
- **Region:** Choose closest to you
- **Branch:** main

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance:**
- **Plan:** Free (or Paid for production)

### Step 5: Add Environment Variables

1. Click "Environment" section
2. Add each variable:

```
GEMINI_API_KEY = your_gemini_api_key
OPENWEATHER_API_KEY = your_openweather_api_key
SECRET_KEY = your_secret_key (generate new)
FLASK_ENV = production
```

3. Click "Create Web Service"

### Step 6: Monitor Deployment

1. Wait 2-5 minutes for build
2. Check logs for errors
3. Once "Live" appears, your app is ready!

### Access Your App

Your app will be at: **https://farmsphere.onrender.com**

---

## Troubleshooting

### Local Development Issues

**Issue: "ModuleNotFoundError: No module named 'flask'"**

Solution:
```bash
pip install -r requirements.txt
```

**Issue: "Port 5000 already in use"**

Solution:
```bash
python app.py --port 5001
```

**Issue: ".env file not found"**

Solution:
```bash
cp .env.example .env
# Add your API keys to .env
```

**Issue: "API keys not working"**

Check:
- Keys are correct (copy exactly)
- .env file is in root directory
- Server restarted after .env changes
- Keys have proper permissions

### Render Deployment Issues

**Issue: "Build failed"**

Check Render logs:
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Look for error messages

Common causes:
- Missing requirements.txt
- Python version mismatch
- Invalid environment variables

**Issue: "Application error"**

Solutions:
1. Check Render logs
2. Verify all environment variables
3. Test locally first
4. Check database connections (if added)

**Issue: "Slow loading"**

Optimization:
1. Use free tier only for testing
2. Upgrade to paid plan for production
3. Implement caching
4. Optimize images

### Image Upload Issues

**Issue: "File too large"**

Solution:
- Maximum file size: 16MB
- Compress images before uploading
- Use PNG/JPG format

**Issue: "Upload button not working"**

Check:
- Browser console for errors (F12)
- uploads/ folder exists
- File format is PNG/JPG/GIF/WEBP

### API Response Issues

**Issue: "Weather data not loading"**

Check:
- API key is correct
- Internet connection is active
- OpenWeatherMap API is accessible
- City name is spelled correctly

**Issue: "Disease diagnosis returns "Unknown""**

Solutions:
- Upload clearer image
- Ensure leaf is main focus
- Try different angle
- Check image quality

---

## Advanced Configuration

### Change Flask Debug Mode

Edit `app.py`:
```python
if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### Add Custom Crops

Edit `app.py` in `CROP_DATABASE`:
```python
'YourCrop': {
    'emoji': '🌾',
    'msp': 2000,
    'season': 'Rabi',
    'rainfall': '100-150mm'
}
```

### Configure CORS

Add to `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

---

## Performance Tips

1. **Optimize Images** - Compress before upload
2. **Enable Caching** - Cache API responses
3. **Lazy Loading** - Load images on scroll
4. **CDN** - Use CDN for static files
5. **Database** - Use for production (PostgreSQL on Render)

---

## Security Checklist

✅ Use environment variables for secrets
✅ Keep SECRET_KEY private
✅ Validate all user inputs
✅ Use HTTPS in production
✅ Implement rate limiting
✅ Regular security updates
✅ Secure API keys

---

## Support Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Render Documentation:** https://render.com/docs
- **Gemini API Docs:** https://ai.google.dev/docs
- **OpenWeatherMap API:** https://openweathermap.org/api

---

## Quick Commands Reference

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Deactivate virtual environment
deactivate

# Push to GitHub
git add .
git commit -m "message"
git push origin main
```

---

**FarmSphere Setup Complete! Happy Farming! 🌾**
