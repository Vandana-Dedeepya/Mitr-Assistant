from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests

app = Flask(__name__)
CORS(app)

# --------- API Key for Weather ----------
WEATHER_API_KEY = "26f2e40b06832ee73c89cd38dc56c64d"

# --------- Intent Detection ----------
def get_intent(user_msg):
    msg = user_msg.lower()
    if any(word in msg for word in ["hi", "hello", "hey", "namaste", "jai"]):
        return "greeting"
    elif "park" in msg or "parking" in msg or "car" in msg:
        return "smart_parking"
    elif "crowd" in msg or "queue" in msg or "rush" in msg:
        return "crowd_prediction"
    elif "language" in msg or "hindi" in msg or "gujarati" in msg or "assistant" in msg:
        return "multilingual"
    elif "weather" in msg:
        return "get_weather"
    elif "help" in msg or "emergency" in msg:
        return "report_emergency"
    elif "time" in msg or "timings" in msg:
        return "get_timings"
    else:
        return "fallback"

# --------- Features ----------
def get_weather(temple="Dwarka"):
    city_map = {
        "Somnath": "Veraval",
        "Dwarka": "Dwarka",
        "Ambaji": "Ambaji",
        "Pavagadh": "Halol"
    }
    city = city_map.get(temple, "Dwarka")
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"🌤️ Weather at {temple}: {temp}°C, {desc}."
        else:
            return f"❌ Could not fetch weather for {temple}."
    except:
        return f"❌ Error fetching weather for {temple}."

def get_crowd_status(temple="Dwarka"):
    capacity_map = {
        "Somnath": 5000,
        "Dwarka": 4500,
        "Ambaji": 6000,
        "Pavagadh": 4000
    }
    capacity = capacity_map.get(temple, 5000)
    current_crowd = random.randint(int(capacity * 0.4), capacity)
    status = "Normal"
    if current_crowd > capacity * 0.8:
        status = "High"
    elif current_crowd > capacity * 0.6:
        status = "Moderate"
    return f"📊 Crowd at {temple}: {current_crowd}/{capacity} ({status}).\n👉 For full details, visit: https://ysabhiram23.github.io/Pilgrim-Guard/"

def get_parking_status():
    total_slots = 50
    available = random.randint(5, total_slots)
    return f"🚗 Parking Availability: {available}/{total_slots} slots free.\n👉 Book here: https://ysabhiram23.github.io/Smart-Parking-System/"

def get_multilingual_help():
    return "🗣️ Our assistant supports Hindi, Gujarati & English.\n👉 Try it here: https://ysabhiram23.github.io/Voice-Assistant/"

def get_timings(temple="Dwarka"):
    timings = {
        "Somnath": "6:00 AM - 9:00 PM",
        "Dwarka": "6:30 AM - 9:30 PM",
        "Ambaji": "7:00 AM - 8:00 PM",
        "Pavagadh": "5:00 AM - 7:00 PM"
    }
    return f"🕑 Timings of {temple}: {timings.get(temple, '6:00 AM - 9:00 PM')}."

def get_greeting():
    return ("🙏 Namaste! I am *Mitr* (मित्र) – your divine assistant. \n\n"
            "🌸 I provide live updates about 4 sacred temples:<br>"
            "1️⃣ Somnath Jyotirlinga<br>"
            "2️⃣ Dwarkadhish Temple<br>"
            "3️⃣ Ambaji Temple<br>"
            "4️⃣ Pavagadh Temple<br><br>"
            "✨ Ask me about crowd status, parking, weather, timings, or emergencies.")

# --------- Chatbot Logic ----------
def chatbot_response(user_msg):
    intent = get_intent(user_msg)
    msg = user_msg.lower()

    if intent == "greeting":
        return get_greeting()

    elif intent == "smart_parking":
        return get_parking_status()

    elif intent == "crowd_prediction":
        if "somnath" in msg:
            return get_crowd_status("Somnath")
        elif "dwarka" in msg:
            return get_crowd_status("Dwarka")
        elif "ambaji" in msg:
            return get_crowd_status("Ambaji")
        elif "pavagadh" in msg:
            return get_crowd_status("Pavagadh")
        else:
            return get_crowd_status("Dwarka")

    elif intent == "multilingual":
        return get_multilingual_help()

    elif intent == "get_weather":
        if "somnath" in msg:
            return get_weather("Somnath")
        elif "dwarka" in msg:
            return get_weather("Dwarka")
        elif "ambaji" in msg:
            return get_weather("Ambaji")
        elif "pavagadh" in msg:
            return get_weather("Pavagadh")
        else:
            return get_weather("Dwarka")

    elif intent == "get_timings":
        if "somnath" in msg:
            return get_timings("Somnath")
        elif "dwarka" in msg:
            return get_timings("Dwarka")
        elif "ambaji" in msg:
            return get_timings("Ambaji")
        elif "pavagadh" in msg:
            return get_timings("Pavagadh")
        else:
            return get_timings("Dwarka")

    elif intent == "report_emergency":
        return "🚨 Emergency reported! Security has been alerted and will assist you immediately."

    else:
        return ("🤖 Sorry, I didn’t understand. You can ask about:\n"
                "- 🚗 Parking\n- 📊 Crowd\n- 🌤️ Weather\n- 🕑 Timings\n- 🗣️ Multilingual Assistant\n- 🚨 Emergencies")

# --------- Flask Route ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chatbot_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
