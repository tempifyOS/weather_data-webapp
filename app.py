from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote_plus

app = Flask(__name__, template_folder='templates', static_folder='static')

def c_to_f(c):
    return round(c * 9/5 + 32, 1) if c is not None else None

def kmh_to_mph(kmh):
    return round(kmh * 0.621371, 1) if kmh is not None else None

def try_geocode(query):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote_plus(query)}&count=1"
    resp = requests.get(url, timeout=8)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if "results" in data and data["results"]:
        return data["results"][0]
    return None

def geocode_location(name: str):
    result = try_geocode(name)
    if result:
        return result
    if "," in name:
        result = try_geocode(name.split(",")[0])
        if result:
            return result
    parts = name.replace(",", "").split()
    if len(parts) >= 2:
        result = try_geocode(" ".join(parts[:-1]))
        if result:
            return result
    raise ValueError("Location not found")

def fetch_weather_all(location_query, unit="metric"):
    geo = geocode_location(location_query)
    lat = geo["latitude"]
    lon = geo["longitude"]
    tz = geo.get("timezone", "auto")

    temp_unit = "fahrenheit" if unit == "imperial" else "celsius"
    windspeed_unit = "mph" if unit == "imperial" else "kmh"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "temperature_2m,precipitation_probability,winddirection_10m,windspeed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": tz,
        "temperature_unit": temp_unit,
        "windspeed_unit": windspeed_unit,
    }
    resp = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=8)
    resp.raise_for_status()
    data = resp.json()

    wc_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        80: "Rain showers", 95: "Thunderstorm"
    }

    current = data.get("current_weather", {})
    daily = data.get("daily", {})
    forecast = []
    for i in range(min(7, len(daily.get("time", [])))):
        forecast.append({
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "weather": wc_map.get(daily["weathercode"][i], "Unknown")
        })

    weather_data = {
        "location": location_query,
        "latitude": lat,
        "longitude": lon,
        "timezone": tz,
        "current": current,
        "forecast": forecast
    }
    return weather_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    location_input = request.form.get('location')
    unit = request.form.get('unit', 'metric')
    try:
        weather_data = fetch_weather_all(location_input, unit)
        print(weather_data)  # Debugging output
        return render_template('weather.html', weather=weather_data)
    except Exception as e:
        error_msg = str(e)
        return render_template('index.html', error=error_msg)

@app.route('/api/weather', methods=['GET'])
def api_weather():
    location = request.args.get('location')
    unit = request.args.get('unit', 'metric')
    try:
        weather_data = fetch_weather_all(location, unit)
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)