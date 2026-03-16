# FarmSphere - AI-Powered Smart Farming Platform

## 🌾 Overview

FarmSphere is a production-ready AI-powered agricultural platform that helps farmers with:

- **🔍 Crop Disease Detection** - Upload plant images for instant AI diagnosis
- **💰 Price Prediction** - ML-based crop price forecasting
- **🌤️ Weather Intelligence** - Real-time forecasts with farming recommendations
- **💬 AI Chatbot** - 24/7 farming advice powered by Gemini AI
- **📊 Analytics Dashboard** - Real-time market trends and crop analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### Local Installation

1. **Clone and Navigate**
```bash
cd FarmSphere
```

2. **Create Virtual Environment** (Optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run Locally**
```bash
python app.py
```

Open your browser: `http://localhost:5000`

## 📋 Environment Setup

Create a `.env` file with these variables:

```env
# Gemini API Key (Get from https://makersuite.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenWeatherMap API Key (Get from https://openweathermap.org/api)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
PORT=5000
```

### Getting API Keys

**Gemini API:**
1. Go to https://makersuite.google.com/
2. Click "Get API Key"
3. Create new API key
4. Copy and paste in .env

**OpenWeatherMap API:**
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get API key from settings
4. Add to .env

## 📁 Project Structure

```
FarmSphere/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Procfile              # Render deployment config
├── render.yaml           # Render service config
│
├── models/               # Pre-trained ML models
│   ├── disease_model.h5  # TensorFlow disease detection model
│   └── price_model.pkl   # Scikit-learn price prediction model
│
├── ai/                   # AI modules
│   ├── __init__.py
│   └── chatbot.py        # Gemini AI chatbot
│
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── weather_api.py    # OpenWeatherMap integration
│   ├── predictor.py      # ML price prediction
│   └── image_classifier.py # Disease detection
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet (glassmorphism design)
│   ├── js/
│   │   ├── main.js
│   │   ├── dashboard.js
│   │   ├── disease.js
│   │   ├── weather.js
│   │   ├── price.js
│   │   └── chatbot.js
│   └── images/           # Image assets
│
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Analytics dashboard
│   ├── disease.html      # Disease diagnosis
│   ├── weather.html      # Weather forecast
│   ├── price_prediction.html # Price prediction
│   └── chatbot.html      # AI chatbot
│
└── uploads/              # Uploaded images (auto-created)
```

## 🎯 Core Features

### 1. Disease Diagnosis
- Upload clear plant leaf images
- AI analyzes and detects diseases
- Shows treatment recommendations
- Provides fertilizer suggestions
- Displays prevention strategies

**Supported Diseases:**
- Early Blight
- Late Blight
- Powdery Mildew
- Leaf Spot
- Healthy crops

### 2. Price Prediction
- Select crop, market, and season
- ML model predicts prices
- Shows 12-month trend chart
- Compares with MSP (Minimum Support Price)
- Market analysis and recommendations

**Supported Crops:**
Wheat, Rice, Maize, Soybean, Cotton, Sugarcane, Mustard, Tomato

**Supported Markets:**
Pune, Mumbai, Nagpur, Indore, Delhi, Bangalore, Chennai, Kolkata

### 3. Weather Integration
- Real-time weather data
- 7-day forecast
- Farming-specific recommendations
- Alerts for disease risk
- Wind and humidity warnings

### 4. AI Chatbot
- 24/7 farming advice
- Crop disease guidance
- Irrigation recommendations
- Fertilizer suggestions
- Market insights
- Best practices

### 5. Analytics Dashboard
- Real-time market trends
- Weather summary
- Crop health analytics
- Price trend charts
- AI-generated insights

## 🔧 API Endpoints

### Dashboard
- `GET /api/dashboard-stats?city=Delhi` - Dashboard statistics

### Weather
- `POST /api/weather` - Current weather data
- `POST /api/forecast` - 7-day forecast

### Disease Detection
- `POST /api/disease/upload` - Upload and analyze image

### Price Prediction
- `POST /api/price/predict` - Predict crop price
- `GET /api/crop-recommendation` - Crop recommendations

### Chatbot
- `POST /api/chat` - Send message to AI chatbot

### General
- `GET /api/farm-tips` - Get farming tips

## 🚢 Deployment on Render

### Step 1: Prepare Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/FarmSphere.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** farmsphere
   - **Environment:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

### Step 3: Add Environment Variables

In Render dashboard:
1. Go to Environment
2. Add each variable from `.env.example`
3. Deploy

### Step 4: Visit Your App

Your app will be live at: `https://farmsphere.onrender.com`

## 📊 Technology Stack

**Backend:**
- Python 3.11
- Flask 3.0
- Scikit-learn (ML)
- TensorFlow/Keras (Deep Learning)
- Gunicorn (Production server)

**Frontend:**
- HTML5
- CSS3 (Glassmorphism design)
- JavaScript (Vanilla)
- Chart.js (Data visualization)

**APIs:**
- Google Generative AI (Gemini) - Chatbot
- OpenWeatherMap - Weather data
- data.gov.in (Optional) - Market prices

**Deployment:**
- Render.com (Production)
- GitHub (Version control)

## 🎨 UI/UX Features

- **Glassmorphism Design** - Modern, frosted glass aesthetic
- **Responsive Layout** - Works on desktop, tablet, mobile
- **Animated Transitions** - Smooth, professional animations
- **Dark Mode Ready** - Can be extended with dark theme
- **Interactive Charts** - Real-time data visualization
- **Quick Actions** - One-click access to key features

## 🔒 Security

- Environment variables for sensitive data
- CORS headers configured
- Input validation on all forms
- File upload restrictions (image files only)
- Rate limiting ready (can be added)

## 📈 Performance

- Lazy loading for images
- Optimized CSS and JavaScript
- Caching strategies implemented
- CDN for Chart.js library
- Fast API response times

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "API Key not working"
- Check `.env` file exists
- Verify API keys are correct
- Restart Flask server

### Issue: "Weather data not loading"
- Check internet connection
- Verify `OPENWEATHER_API_KEY` is set
- Check Render logs for errors

### Issue: "Image upload fails"
- Ensure image format is PNG, JPG, JPEG, GIF, or WEBP
- Check file size is under 16MB
- Check `uploads/` folder exists

## 📚 Documentation

### Adding New Crops

Edit `CROP_DATABASE` in `app.py`:
```python
CROP_DATABASE = {
    'Crop_Name': {
        'emoji': '🌾',
        'msp': 2275,
        'season': 'Rabi',
        'rainfall': '100-150mm'
    }
}
```

### Adding New Diseases

Edit `DISEASE_DATABASE` in `app.py`:
```python
DISEASE_DATABASE = {
    'Disease_Name': {
        'treatment': 'Treatment recommendations',
        'fertilizer': 'Fertilizer guidance',
        'prevention': 'Prevention methods'
    }
}
```

### Customizing Chat Responses

Edit `FarmSphereChatbot` class in `ai/chatbot.py`:
```python
def get_fallback_response(self, message):
    # Add custom responses here
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - feel free to use for personal and commercial projects

## 👨‍💻 Support

For issues and questions:
1. Check GitHub Issues
2. Review API documentation
3. Check Render logs: `render.com/dashboard`

## 🌟 Future Enhancements

- [ ] SMS/WhatsApp integration for alerts
- [ ] Mobile app (React Native)
- [ ] IoT sensor integration
- [ ] Multilingual support
- [ ] Offline mode
- [ ] Advanced analytics
- [ ] Farmer community forum
- [ ] Government scheme updates

## 📞 Contact

For support and collaboration:
- Email: support@farmsphere.ai
- Website: www.farmsphere.ai

---

**FarmSphere** - Empowering farmers with AI 🌾
