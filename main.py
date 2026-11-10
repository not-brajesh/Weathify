import os
import requests
from datetime import datetime, timedelta

# Configurations GitHub Actions env se aayengi
CITY = os.getenv("CITY", "Pune")
LAT = os.getenv("LAT", "18.5204")
LON = os.getenv("LON", "73.8567")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

def get_tomorrow_weather():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Open-Meteo API call
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}&daily=weathercode,temperature_2m_max,temperature_2m_min,"
        f"precipitation_probability_max,windspeed_10m_max&timezone=Asia%2FKolkata"
    )
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Tomorrow ka index find karna
    idx = data["daily"]["time"].index(tomorrow)
    
    temp_max = data["daily"]["temperature_2m_max"][idx]
    temp_min = data["daily"]["temperature_2m_min"][idx]
    rain_prob = data["daily"]["precipitation_probability_max"][idx]
    wind_speed = data["daily"]["windspeed_10m_max"][idx]
    code = data["daily"]["weathercode"][idx]

    # Weather conditions
    wmo_codes = {
        0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
        45: "Fog 🌫️", 48: "Depositing rime fog 🌫️",
        51: "Light drizzle 🌦️", 53: "Moderate drizzle 🌧️", 55: "Dense drizzle 🌧️",
        61: "Slight rain 🌦️", 63: "Moderate rain 🌧️", 65: "Heavy rain ⛈️",
        71: "Slight snow 🌨️", 73: "Moderate snow ❄️", 75: "Heavy snow ❄️",
        80: "Slight rain showers 🌦️", 81: "Moderate rain showers 🌧️", 82: "Violent rain showers ⛈️",
        95: "Thunderstorm 🌩️"
    }
    weather_desc = wmo_codes.get(code, "Unknown condition")

    return (
        f"🌤️ *Tomorrow's Weather in {CITY}*\n\n"
        f"Condition: {weather_desc}\n"
        f"🌡️ Max Temp: {temp_max}°C\n"
        f"❄️ Min Temp: {temp_min}°C\n"
        f"🌧️ Rain Probability: {rain_prob}%\n"
        f"💨 Wind Speed: {wind_speed} km/h\n\n"
        f"Have a great day ahead! 🚀"
    )

def send_whatsapp(message):
    if not all([WHATSAPP_TOKEN, PHONE_NUMBER_ID, WHATSAPP_TO]):
        print("WhatsApp credentials missing. Skipping message send.")
        return

    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_TO,
        "type": "text",
        "text": {"body": message}
    }
    
    r = requests.post(url, headers=headers, json=payload)
    print("WhatsApp Response:", r.text)

if __name__ == "__main__":
    print("Fetching weather...")
    report = get_tomorrow_weather()
    print(report)
    
    print("\nSending WhatsApp notification...")
    send_whatsapp(report)
