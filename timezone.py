# Flask Backend for World Time API
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# A mapping of country names to their capital cities
COUNTRY_CAPITALS = {
    'egypt': 'Cairo',
    'united states': 'Washington',
    'usa': 'Washington',
    'france': 'Paris',
    'germany': 'Berlin',
    'japan': 'Tokyo',
    'china': 'Beijing',
    'india': 'New Delhi',
    'brazil': 'Brasilia',
    'canada': 'Ottawa',
    'australia': 'Canberra',
    'russia': 'Moscow',
    'uk': 'London',
    'united kingdom': 'London',
    'italy': 'Rome',
    'spain': 'Madrid',
    'saudi arabia': 'Riyadh',
    'turkey': 'Ankara',
    'south africa': 'Pretoria',
}

# A mapping of capital cities to their coordinates (latitude, longitude)
CITY_COORDS = {
    'Cairo': (30.0444, 31.2357),
    'Washington': (38.89511, -77.03637),
    'Paris': (48.8566, 2.3522),
    'Berlin': (52.52, 13.405),
    'Tokyo': (35.6895, 139.6917),
    'Beijing': (39.9042, 116.4074),
    'New Delhi': (28.6139, 77.209),
    'Brasilia': (-15.7939, -47.8828),
    'Ottawa': (45.4215, -75.6996),
    'Canberra': (-35.2809, 149.13),
    'Moscow': (55.7558, 37.6173),
    'London': (51.5074, -0.1278),
    'Rome': (41.9028, 12.4964),
    'Madrid': (40.4168, -3.7038),
    'Riyadh': (24.7136, 46.6753),
    'Ankara': (39.9334, 32.8597),
    'Pretoria': (-25.7479, 28.2293),
}

# Country data with timezone information
COUNTRY_DATA = {
    'egypt': { 'name': 'Egypt', 'city': 'Cairo', 'timezone': 'Africa/Cairo' },
    'usa': { 'name': 'United States', 'city': 'Washington', 'timezone': 'America/New_York' },
    'france': { 'name': 'France', 'city': 'Paris', 'timezone': 'Europe/Paris' },
    'germany': { 'name': 'Germany', 'city': 'Berlin', 'timezone': 'Europe/Berlin' },
    'japan': { 'name': 'Japan', 'city': 'Tokyo', 'timezone': 'Asia/Tokyo' },
    'china': { 'name': 'China', 'city': 'Beijing', 'timezone': 'Asia/Shanghai' },
    'india': { 'name': 'India', 'city': 'New Delhi', 'timezone': 'Asia/Kolkata' },
    'brazil': { 'name': 'Brazil', 'city': 'Brasília', 'timezone': 'America/Sao_Paulo' },
    'canada': { 'name': 'Canada', 'city': 'Ottawa', 'timezone': 'America/Toronto' },
    'australia': { 'name': 'Australia', 'city': 'Canberra', 'timezone': 'Australia/Sydney' },
    'russia': { 'name': 'Russia', 'city': 'Moscow', 'timezone': 'Europe/Moscow' },
    'uk': { 'name': 'United Kingdom', 'city': 'London', 'timezone': 'Europe/London' },
    'italy': { 'name': 'Italy', 'city': 'Rome', 'timezone': 'Europe/Rome' },
    'spain': { 'name': 'Spain', 'city': 'Madrid', 'timezone': 'Europe/Madrid' },
    'saudi arabia': { 'name': 'Saudi Arabia', 'city': 'Riyadh', 'timezone': 'Asia/Riyadh' },
    'turkey': { 'name': 'Turkey', 'city': 'Ankara', 'timezone': 'Europe/Istanbul' },
    'south africa': { 'name': 'South Africa', 'city': 'Pretoria', 'timezone': 'Africa/Johannesburg' }
}

tf = TimezoneFinder()

def get_timezone(country):
    """Get timezone and city for a given country"""
    country = country.strip().lower()
    
    # First try direct lookup from COUNTRY_DATA
    if country in COUNTRY_DATA:
        data = COUNTRY_DATA[country]
        return data['timezone'], data['city']
    
    # Fallback to old method if not found
    city = COUNTRY_CAPITALS.get(country)
    if not city:
        return None, None
    coords = CITY_COORDS.get(city)
    if not coords:
        return None, None
    lat, lng = coords
    tz_name = tf.timezone_at(lng=lng, lat=lat)
    return tz_name, city

def format_time_response(country, tz_name, city):
    """Format time response for a country"""
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        
        return {
            'success': True,
            'country': country.title(),
            'city': city,
            'timezone': tz_name,
            'time': now.strftime('%Y-%m-%d %H:%M:%S'),
            'formatted_time': now.strftime('%I:%M:%S %p'),
            'date': now.strftime('%Y-%m-%d'),
            'timestamp': now.timestamp()
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error getting time for {country.title()}: {str(e)}'
        }

# API Routes

@app.route('/')
def index():
    """Serve the main page from templates/index.html"""
    # Serve the static template file placed under templates/
    return render_template('index.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get list of all available countries"""
    countries = []
    for key, data in COUNTRY_DATA.items():
        countries.append({
            'key': key,
            'name': data['name'],
            'city': data['city'],
            'timezone': data['timezone']
        })
    
    return jsonify({
        'success': True,
        'countries': countries,
        'total': len(countries)
    })

@app.route('/api/time/<country>', methods=['GET'])
def get_country_time_get(country):
    """Get current time for a specific country (GET method)"""
    tz_name, city = get_timezone(country)
    
    if not tz_name:
        return jsonify({
            'success': False,
            'error': f"Sorry, I don't know the timezone for '{country}'. Try using the country key or capital city name.",
            'available_countries': list(COUNTRY_DATA.keys())
        }), 404
    
    return jsonify(format_time_response(country, tz_name, city))

@app.route('/api/time', methods=['POST'])
def get_country_time_post():
    """Get current time for a country (POST method)"""
    try:
        data = request.get_json()
        if not data or 'country' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: country'
            }), 400
        
        country = data['country']
        tz_name, city = get_timezone(country)
        
        if not tz_name:
            return jsonify({
                'success': False,
                'error': f"Sorry, I don't know the timezone for '{country}'. Try using the country key or capital city name.",
                'available_countries': list(COUNTRY_DATA.keys())
            }), 404
        
        return jsonify(format_time_response(country, tz_name, city))
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Invalid request: {str(e)}'
        }), 400

@app.route('/api/compare', methods=['POST'])
def compare_countries():
    """Compare times between two countries"""
    try:
        data = request.get_json()
        if not data or 'country1' not in data or 'country2' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: country1 and country2'
            }), 400
        
        country1 = data['country1']
        country2 = data['country2']
        
        if country1.lower() == country2.lower():
            return jsonify({
                'success': False,
                'error': 'Please provide two different countries'
            }), 400
        
        # Get timezone info for both countries
        tz1, city1 = get_timezone(country1)
        tz2, city2 = get_timezone(country2)
        
        if not tz1 or not tz2:
            missing = []
            if not tz1:
                missing.append(country1)
            if not tz2:
                missing.append(country2)
            
            return jsonify({
                'success': False,
                'error': f"Unknown timezone for: {', '.join(missing)}",
                'available_countries': list(COUNTRY_DATA.keys())
            }), 404
        
        try:
            now_utc = datetime.now(pytz.utc)
            
            tz1_obj = pytz.timezone(tz1)
            tz2_obj = pytz.timezone(tz2)
            
            # Convert UTC time to local times
            time1 = now_utc.astimezone(tz1_obj)
            time2 = now_utc.astimezone(tz2_obj)
            
            # Calculate offset difference
            offset1 = time1.utcoffset().total_seconds()
            offset2 = time2.utcoffset().total_seconds()
            
            diff_seconds = abs(offset1 - offset2)
            diff_hours = int(diff_seconds // 3600)
            diff_minutes = int((diff_seconds % 3600) // 60)
            
            return jsonify({
                'success': True,
                'country1': {
                    'name': country1.title(),
                    'city': city1,
                    'timezone': tz1,
                    'time': time1.strftime('%Y-%m-%d %H:%M:%S'),
                    'formatted_time': time1.strftime('%I:%M:%S %p'),
                    'timestamp': time1.timestamp()
                },
                'country2': {
                    'name': country2.title(),
                    'city': city2,
                    'timezone': tz2,
                    'time': time2.strftime('%Y-%m-%d %H:%M:%S'),
                    'formatted_time': time2.strftime('%I:%M:%S %p'),
                    'timestamp': time2.timestamp()
                },
                'time_difference': {
                    'hours': diff_hours,
                    'minutes': diff_minutes,
                    'total_minutes': int(diff_seconds // 60),
                    'same_timezone': diff_hours == 0 and diff_minutes == 0,
                    'description': f"{diff_hours} hours and {diff_minutes} minutes" if diff_hours > 0 or diff_minutes > 0 else "Same timezone"
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error calculating time difference: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Invalid request: {str(e)}'
        }), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'GET /api/countries',
            'GET /api/time/<country>',
            'POST /api/time',
            'POST /api/compare'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed for this endpoint'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🌍 World Time API Server Starting...")
    print("📝 API Documentation: http://localhost:5000/")
    print("🚀 Server running on: http://localhost:5000/")
    print("\n📋 Available endpoints:")
    print("   GET  /api/countries")
    print("   GET  /api/time/<country>")
    print("   POST /api/time")
    print("   POST /api/compare")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
