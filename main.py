import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
from openai import OpenAI

# ----------------------------
# Load secrets from .env
# ----------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TO_SMS = os.getenv("TO_SMS")
FROM_SMS = os.getenv("TWILIO_FROM_SMS")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")
FROM_WHATSAPP = os.getenv("TWILIO_FROM_WHATSAPP")

client_openai = OpenAI(api_key=OPENAI_API_KEY)
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ----------------------------
# Step 1: Get weather data
# ----------------------------
def get_weather(city="Hyderabad"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# ----------------------------
# Step 2: Summarize in farmer-friendly way
# ----------------------------
def generate_advice(weather_json, lang="te"):  # default Telugu
    description = weather_json["weather"][0]["description"]
    temp = weather_json["main"]["temp"]
    wind = weather_json["wind"]["speed"]

    raw_text = f"""
    Weather Report:
    - Temperature: {temp}°C
    - Condition: {description}
    - Wind Speed: {wind} m/s

    Give a short farmer-friendly advice in {lang} language.
    """

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an agriculture assistant."},
                  {"role": "user", "content": raw_text}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# ----------------------------
# Step 3: Send Alerts
# ----------------------------
def send_sms(message):
    client_twilio.messages.create(
        body=message,
        from_=FROM_SMS,
        to=TO_SMS
    )

def send_whatsapp(message):
    client_twilio.messages.create(
        body=message,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )

# ----------------------------
# MAIN FLOW
# ----------------------------
if __name__ == "__main__":
    weather = get_weather("Hyderabad")  # change city here
    advice = generate_advice(weather, lang="hi")  # "hi"=Hindi, "te"=Telugu
    print("Farmer Advice:", advice)

    # Send alerts
    send_sms(advice)
    send_whatsapp(advice)
    print("✅ Alerts sent successfully!")
from openai import OpenAI

client = OpenAI(api_key="your_actual_api_key_here")
