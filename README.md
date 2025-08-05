
# Weather Data Web Application

A responsive, light-weight Flask web application for looking up current and 7-day forecast weather data for any location, with built-in dark/light theming and unit switching (°F/°C). Leveraging Open-Meteo’s APIs for geocoding and forecast data, this app features:

* Dynamic Search by city name or lat/lon

* Current Conditions (temp, humidity, wind, description)

* 7-Day Forecast cards

* Dark/Light Mode with system-prefers-color-scheme detection

* Unit Toggle between Fahrenheit and Celsius (currently broken)

* Google App Engine–ready deployment




## Tech Stack

* Backend: Python 3.10, Flask

* Frontend: HTML5, Tailwind-inspired CSS variables, vanilla JavaScript

* APIs:

   &nbsp;1. Open-Meteo Geocoding API

     &nbsp;2. Open-Meteo Forecast API
     
    &nbsp;3. NASA’s LARC-POWER API
     

* Deployment: Google App Engine (standard environment)

* Process: gunicorn WSGI server

## Run Locally
Prerequisites
* Python 3.10+
* gcloud CLI (deployment)

Clone & activate the project

```bash
  git clone git@github.com:tempifyOS/weather_data-webapp.git
  cd weather_data-webapp
  python -m venv venv
  source venv/bin/activate
```


Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server locally

```bash
  export FLASK_APP=app.py
  flask run --host=0.0.0.0 --port=8080
```


## 📂 Project Structure

├── app.py               # Flask routes & weather‐fetch logic\
├── app.yaml             # GAE configuration\
├── requirements.txt     # Python dependencies\
├── static/\
│   └── styles.css       # Shared CSS variables & utility classes\
└── templates/\
&nbsp;    ├── index.html       # Landing & search page\
&nbsp;    └── weather.html     # Results page with forecast cards\


