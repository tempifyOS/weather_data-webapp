from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__, template_folder='templates',static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=[POST])
def weather():
    location_input = request.form['location']
    lat, lon = parse_location(location_input)
    weather_data = get_weather_data(lat, lon)
    
    return render_template('weather.html', weather=weather_data)

def parse_location(location_input):
    input = location_input.strip()
    # determine if input is coordinates
    if ',' in input and all(part.strip().replace('.', '', 1).replace('-', '', 1).isdigit() for part in input.split(',')):
        lat, lon = map(float, input.split(','))
    else:
        convert_to_coordinates(input)
    return lat, lon

def convert_to_coordinates(location_input):
    # convert 'city' or 'city, state' to coordinates
    return lat, lon

def get_weather_data(lat, lon):
    # call NASA api for weather data
    return weather_data

if __name__ == '__main__':
    # local dev with auto‑reload and debug info
    app.run(host='0.0.0.0', port=8080, debug=True)