import requests
import matplotlib.pyplot as plt

def get_coordinates(city):
    """Get latitude & longitude from Open-Meteo Geocoding API (no key)."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    data = requests.get(url).json()

    if "results" not in data:
        return None, None

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon


def get_air_quality(lat, lon):
    """Fetch air quality data."""
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,carbon_monoxide,"
        f"nitrogen_dioxide,sulphur_dioxide,ozone"
    )

    data = requests.get(url).json()
    hour = 0  # first hour data

    return {
        "PM2.5": data["hourly"]["pm2_5"][hour],
        "PM10": data["hourly"]["pm10"][hour],
        "CO": data["hourly"]["carbon_monoxide"][hour],
        "NO2": data["hourly"]["nitrogen_dioxide"][hour],
        "SO2": data["hourly"]["sulphur_dioxide"][hour],
        "O3": data["hourly"]["ozone"][hour]
    }


def calculate_aqi(pm25):
    """AQI Category using PM2.5."""
    if pm25 <= 30:
        return "Good 😀"
    elif pm25 <= 60:
        return "Satisfactory 🙂"
    elif pm25 <= 90:
        return "Moderate 😐"
    elif pm25 <= 120:
        return "Poor 😷"
    elif pm25 <= 250:
        return "Very Poor 🤢"
    else:
        return "Severe ☠"


# ------------------------------- MAIN PROGRAM --------------------------------

city = input("Enter city name: ")

lat, lon = get_coordinates(city)

if lat is None:
    print("City not found. Try again.")
else:
    pollutants = get_air_quality(lat, lon)

    print("\n----------------------------------")
    print(f"🌍 Air Quality in {city.title()}")
    print("----------------------------------")

    for key, val in pollutants.items():
        print(f"{key} : {val}")

    print("----------------------------------")
    print(f"AQI Category: {calculate_aqi(pollutants['PM2.5'])}")

    # ---------------------- Create Graph ----------------------

    labels = list(pollutants.keys())
    values = list(pollutants.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(f"Air Pollutant Levels in {city.title()}")
    plt.xlabel("Pollutants")
    plt.ylabel("Concentration (μg/m3)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()