import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not set in .env")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            try:
                url = "https://api.openweathermap.org/data/2.5/weather"
                params = {"q": city, "appid": API_KEY, "units": "metric"}
                resp = requests.get(url, params=params, timeout=8)
                data = resp.json()

                if resp.status_code == 200:
                    weather = {
                        "city": f"{data.get('name')}, {data.get('sys', {}).get('country','')}",
                        "temp": data["main"]["temp"],
                        "feels_like": data["main"].get("feels_like"),
                        "description": data["weather"][0]["description"].title(),
                        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                        "humidity": data["main"].get("humidity"),
                        "pressure": data["main"].get("pressure"),
                        "wind_speed": data.get("wind", {}).get("speed"),
                    }
                else:
                    error = data.get("message", "Could not fetch weather")
            except requests.RequestException:
                error = "Network error. Try again."

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
