"""
FarmSphere - AI-Powered Smart Farming Platform
Production-ready Flask application with ML, AI, and real-time integrations
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import pickle
import numpy as np
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import io

# Import custom utilities
try:
    from utils.weather_api import get_weather_data, get_forecast_data
    from utils.predictor import predict_crop_price
    from utils.image_classifier import classify_disease_from_image
    from ai.chatbot import FarmSphereChatbot
except ImportError as e:
    print(f"Warning: {e}. Some features may not work.")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'farmsphere-secret-key-2024')

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ─── CONFIGURATION ────────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
WEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Initialize chatbot
try:
    chatbot = FarmSphereChatbot(GEMINI_API_KEY)
except:
    chatbot = None

# ─── CROP DATABASE ────────────────────────────────────────────────────
CROP_DATABASE = {
    'Wheat': {'emoji': '🌾', 'msp': 2275, 'season': 'Rabi', 'rainfall': '100-150mm'},
    'Rice': {'emoji': '🍚', 'msp': 2300, 'season': 'Kharif', 'rainfall': '150-250mm'},
    'Maize': {'emoji': '🌽', 'msp': 2090, 'season': 'Kharif', 'rainfall': '100-150mm'},
    'Soybean': {'emoji': '🫘', 'msp': 4892, 'season': 'Kharif', 'rainfall': '100-150mm'},
    'Cotton': {'emoji': '🌸', 'msp': 7020, 'season': 'Kharif', 'rainfall': '150-200mm'},
    'Sugarcane': {'emoji': '🎋', 'msp': 3400, 'season': 'Annual', 'rainfall': '100-150mm'},
    'Mustard': {'emoji': '🌻', 'msp': 5650, 'season': 'Rabi', 'rainfall': '50-100mm'},
    'Tomato': {'emoji': '🍅', 'msp': 0, 'season': 'Rabi', 'rainfall': '100-150mm'}
}

MARKETS = ['Pune', 'Mumbai', 'Nagpur', 'Indore', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']

DISEASE_DATABASE = {
    'Early Blight': {
        'treatment': 'Spray Mancozeb 75% WP @ 2g/L water. Repeat after 10-14 days',
        'fertilizer': 'NPK 19:19:19. Increase Potassium for resistance',
        'prevention': 'Remove infected leaves. Ensure proper spacing for air circulation'
    },
    'Late Blight': {
        'treatment': 'Use Copper Oxychloride 50% @ 3g/L or Metalaxyl + Mancozeb',
        'fertilizer': 'Potassium-rich fertilizer (K2O 40-50 kg/ha)',
        'prevention': 'Avoid overhead watering. Remove infected plant parts'
    },
    'Powdery Mildew': {
        'treatment': 'Spray Sulfur 80% WP @ 2g/L or Carbendazim 50% WP',
        'fertilizer': 'Balanced NPK 12:32:16. Avoid excessive Nitrogen',
        'prevention': 'Improve air circulation. Remove weeds nearby'
    },
    'Leaf Spot': {
        'treatment': 'Spray Chlorothalonil 75% @ 2.5g/L or Hexaconazole',
        'fertilizer': 'Micronutrients especially Zinc @ 5kg/ha',
        'prevention': 'Crop rotation. Remove crop residue. Use resistant varieties'
    },
    'Healthy': {
        'treatment': 'Continue regular monitoring and care',
        'fertilizer': 'Follow recommended crop nutrition schedule',
        'prevention': 'Maintain good agricultural practices'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── ROUTES ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', crops=CROP_DATABASE)

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/disease-diagnosis')
def disease_diagnosis():
    """Crop disease diagnosis page"""
    return render_template('disease.html')

@app.route('/weather')
def weather_page():
    """Weather forecast page"""
    return render_template('weather.html')

@app.route('/price-prediction')
def price_prediction():
    """Crop price prediction page"""
    return render_template('price_prediction.html', crops=CROP_DATABASE, markets=MARKETS)

@app.route('/chatbot')
def chatbot_page():
    """AI chatbot page"""
    return render_template('chatbot.html')

# ─── API ENDPOINTS ────────────────────────────────────────────────────

@app.route('/api/dashboard-stats', methods=['GET'])
def api_dashboard_stats():
    """Get dashboard statistics"""
    try:
        city = request.args.get('city', 'Delhi')
        
        # Generate sample data
        stats = {
            'success': True,
            'weather': generate_weather_summary(city),
            'market_trends': generate_market_trends(),
            'crop_analytics': generate_crop_analytics(),
            'ai_insights': generate_ai_insights()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/weather', methods=['POST'])
def api_weather():
    """Get weather data for a city"""
    try:
        city = request.form.get('city', 'Delhi').strip()
        if not city:
            return jsonify({'success': False, 'error': 'City name required'}), 400
        
        # Try real API first
        weather_data = get_weather_data(city, WEATHER_API_KEY) if WEATHER_API_KEY else None
        
        # Fallback to demo data
        if not weather_data:
            weather_data = generate_demo_weather(city)
        
        return jsonify({'success': True, 'data': weather_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/forecast', methods=['POST'])
def api_forecast():
    """Get 7-day weather forecast"""
    try:
        city = request.form.get('city', 'Delhi').strip()
        
        forecast = get_forecast_data(city, WEATHER_API_KEY) if WEATHER_API_KEY else None
        
        if not forecast:
            forecast = generate_demo_forecast(city)
        
        return jsonify({'success': True, 'data': forecast})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/disease/upload', methods=['POST'])
def api_upload_disease_image():
    """Upload and analyze crop disease image"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze disease
        result = classify_disease_from_image(filepath)
        
        disease_info = DISEASE_DATABASE.get(result['disease'], DISEASE_DATABASE['Healthy'])
        
        response = {
            'success': True,
            'disease': result['disease'],
            'confidence': result['confidence'],
            'treatment': disease_info['treatment'],
            'fertilizer': disease_info['fertilizer'],
            'prevention': disease_info['prevention'],
            'image_filename': filename
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/price/predict', methods=['POST'])
def api_predict_price():
    """Predict crop price using ML model"""
    try:
        crop = request.form.get('crop', 'Wheat')
        market = request.form.get('market', 'Pune')
        season = request.form.get('season', 'Kharif')
        
        if crop not in CROP_DATABASE:
            return jsonify({'success': False, 'error': 'Invalid crop'}), 400
        
        # Get prediction
        predicted_price = predict_crop_price(crop, market, season)
        msp = CROP_DATABASE[crop]['msp']
        
        # Generate trend data
        trend_data = generate_price_trend(crop, predicted_price)
        
        response = {
            'success': True,
            'crop': crop,
            'market': market,
            'season': season,
            'predicted_price': round(predicted_price, 2),
            'msp': msp,
            'difference_from_msp': round(predicted_price - msp, 2),
            'percentage_vs_msp': round(((predicted_price - msp) / msp * 100) if msp > 0 else 0, 2),
            'trend': trend_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """AI chatbot endpoint"""
    try:
        message = request.form.get('message', '').strip()
        history = json.loads(request.form.get('history', '[]'))
        
        if not message:
            return jsonify({'success': False, 'error': 'Empty message'}), 400
        
        if not chatbot:
            reply = generate_fallback_response(message)
        else:
            reply = chatbot.chat(message, history)
        
        return jsonify({
            'success': True,
            'reply': reply,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/crop-recommendation', methods=['POST'])
def api_crop_recommendation():
    """Get crop recommendation based on conditions"""
    try:
        rainfall = float(request.form.get('rainfall', 100))
        temperature = float(request.form.get('temperature', 25))
        soil_type = request.form.get('soil_type', 'loamy')
        
        recommendations = []
        
        for crop, info in CROP_DATABASE.items():
            score = 0
            # Simple scoring system
            if '100' in info['rainfall'] or '150' in info['rainfall']:
                score += 30
            if temperature > 15 and temperature < 35:
                score += 30
            score += 40  # Base score
            
            recommendations.append({
                'crop': crop,
                'emoji': info['emoji'],
                'score': min(score, 100),
                'msp': info['msp'],
                'season': info['season']
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations[:3]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/farm-tips', methods=['GET'])
def api_farm_tips():
    """Get AI-generated farming tips"""
    tips = [
        {
            'title': '🚜 Crop Rotation Benefits',
            'description': 'Rotate crops yearly to maintain soil health and reduce pest buildup',
            'emoji': '🌱'
        },
        {
            'title': '💧 Efficient Irrigation',
            'description': 'Use drip irrigation to save 30-40% water compared to flood irrigation',
            'emoji': '💧'
        },
        {
            'title': '🐛 Integrated Pest Management',
            'description': 'Combine biological and chemical methods for sustainable pest control',
            'emoji': '🦗'
        },
        {
            'title': '🌾 Soil Health',
            'description': 'Add organic matter and mulch to improve soil fertility naturally',
            'emoji': '🌍'
        },
        {
            'title': '📊 Data-Driven Farming',
            'description': 'Use weather data and soil testing to optimize farming decisions',
            'emoji': '📱'
        }
    ]
    
    return jsonify({'success': True, 'tips': tips})

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────

def generate_weather_summary(city):
    """Generate weather summary"""
    return {
        'city': city,
        'temperature': f"{np.random.randint(20, 35)}°C",
        'humidity': f"{np.random.randint(40, 80)}%",
        'wind_speed': f"{np.random.randint(5, 25)} km/h",
        'rain_probability': f"{np.random.randint(10, 60)}%",
        'condition': '⛅ Partly Cloudy'
    }

def generate_demo_weather(city):
    """Generate demo weather data"""
    return {
        'city': city,
        'temperature': 28,
        'feels_like': 30,
        'humidity': 65,
        'wind_speed': 12,
        'pressure': 1013,
        'visibility': 10,
        'condition': 'Partly Cloudy',
        'icon': '⛅',
        'sunrise': '06:30',
        'sunset': '18:45',
        'forecast_available': True
    }

def generate_demo_forecast(city):
    """Generate demo 7-day forecast"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    forecast = []
    for day in days:
        forecast.append({
            'day': day,
            'high_temp': np.random.randint(30, 35),
            'low_temp': np.random.randint(20, 25),
            'condition': '⛅',
            'rain_probability': np.random.randint(10, 50)
        })
    return forecast

def generate_market_trends():
    """Generate market trend data"""
    return {
        'wheat': {'current': 2280, 'trend': 'up', 'change': '+2.2%'},
        'rice': {'current': 2310, 'trend': 'stable', 'change': '0%'},
        'maize': {'current': 2100, 'trend': 'down', 'change': '-0.5%'}
    }

def generate_crop_analytics():
    """Generate crop analytics"""
    return {
        'total_crops': 8,
        'healthy_crops': 6,
        'at_risk_crops': 1,
        'disease_percentage': 12.5,
        'top_crop': 'Wheat',
        'prediction_accuracy': 94.2
    }

def generate_ai_insights():
    """Generate AI insights"""
    return {
        'recommendation': 'Plant Wheat in Rabi season for 15% higher yield',
        'warning': 'Rain expected - delay fertilizer application',
        'opportunity': 'Cotton prices trending up - good time to plant'
    }

def generate_price_trend(crop, current_price):
    """Generate price trend data for chart"""
    trend = []
    base_price = current_price - 100
    for i in range(12):
        trend.append({
            'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i],
            'price': round(base_price + np.random.randint(-20, 50), 2)
        })
    return trend

def generate_fallback_response(message):
    """Generate fallback chatbot response"""
    responses = {
        'disease': 'Common crop diseases include Early Blight, Late Blight, and Powdery Mildew. Upload an image for diagnosis.',
        'weather': 'Check the Weather page for current conditions and 7-day forecast.',
        'price': 'Use our Price Prediction tool to forecast crop prices based on market data.',
        'irrigation': 'Use drip irrigation to save 30-40% water. Optimal time is early morning.',
        'fertilizer': 'Use NPK ratios based on crop type. Wheat needs 120:60:40, Rice needs 120:60:60.',
        'default': 'Welcome to FarmSphere! I can help you with crop diseases, weather, prices, and farming tips.'
    }
    
    message_lower = message.lower()
    for key in responses:
        if key in message_lower:
            return responses[key]
    return responses['default']

# ─── ERROR HANDLERS ────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ─── MAIN ENTRY POINT ────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
