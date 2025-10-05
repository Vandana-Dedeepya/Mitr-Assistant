'''from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dummy data for temples
temples = {
    "somnath": {
        "timings": "Somnath Temple is open from 6 AM to 9 PM.",
        "booking": "You can book tickets at the official Somnath trust website.",
        "emergency": "In case of emergency at Somnath, call 100 or 108."
    },
    "dwarka": {
        "timings": "Dwarka Temple is open from 6:30 AM to 1 PM and 5 PM to 9:30 PM.",
        "booking": "Online booking for Dwarka is available on the temple’s official portal.",
        "emergency": "For emergencies at Dwarka, call 100 or 108."
    },
    "pavagadh": {
        "timings": "Pavagadh Temple is open from 5 AM to 7 PM.",
        "booking": "Tickets for ropeway and entry are available at the temple counters.",
        "emergency": "In case of emergency at Pavagadh, call 100 or 108."
    },
    "ambaji": {
        "timings": "Ambaji Temple is open from 6 AM to 12 PM and 3 PM to 9 PM.",
        "booking": "You can book online tickets for Ambaji through the Gujarat tourism website.",
        "emergency": "For emergencies at Ambaji, call 100 or 108."
    }
}

# Weather API
API_KEY = "26f2e40b06832ee73c89cd38dc56c64d"
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"🌤️ Weather at {city.capitalize()}: {temp}°C, {desc}."
    else:
        return f"❌ Could not fetch weather for {city}."

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Match temple
    for temple in temples.keys():
        if temple in user_message:
            # Check for intent
            if "time" in user_message or "timing" in user_message or "open" in user_message:
                return jsonify({"reply": temples[temple]["timings"]})
            elif "book" in user_message or "ticket" in user_message or "booking" in user_message:
                return jsonify({"reply": temples[temple]["booking"]})
            elif "emergency" in user_message or "help" in user_message:
                return jsonify({"reply": temples[temple]["emergency"]})
            elif "weather" in user_message:
                return jsonify({"reply": get_weather(temple)})
            else:
                return jsonify({"reply": f"ℹ️ What do you want to know about {temple.capitalize()}? (timings, booking, weather, emergency)"})

    # Fallback
    return jsonify({"reply": "🤖 Sorry, I didn’t understand. You can ask about wait time, booking, emergencies, weather, or crowd."})

if __name__ == "__main__":
    app.run(debug=True)'''

'''from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
from fuzzywuzzy import process

app = Flask(__name__)
CORS(app)  # Allow frontend calls

# --------- API Key ----------
WEATHER_API_KEY = "26f2e40b06832ee73c89cd38dc56c64d"  # replace with yours

# --------- Temple Data ----------
temples = ["Somnath", "Dwarka", "Ambaji", "Pavagadh"]
city_map = {
    "Somnath": "Veraval",
    "Dwarka": "Dwarka",
    "Ambaji": "Ambaji",
    "Pavagadh": "Halol"
}
capacity_map = {
    "Somnath": 5000,
    "Dwarka": 4500,
    "Ambaji": 6000,
    "Pavagadh": 4000
}

# --------- Intent Detection ----------
def get_intent(user_msg):
    msg = user_msg.lower()
    if "wait" in msg or "queue" in msg:
        return "ask_wait_time"
    elif "book" in msg or "token" in msg or "darshan" in msg:
        return "book_darshan"
    elif "emergency" in msg or "help" in msg:
        return "report_emergency"
    elif "weather" in msg:
        return "get_weather"
    elif "crowd" in msg:
        return "get_crowd"
    elif "temples" in msg or "options" in msg:
        return "list_temples"
    else:
        return "fallback"

# --------- Fuzzy Temple Matching ----------
def match_temple(user_msg):
    choice, score = process.extractOne(user_msg, temples)
    if score > 70:
        return choice
    return None

# --------- Real-Time API Functions ----------
def get_weather(temple="Dwarka"):
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

def get_crowd_status(temple="Somnath"):
    capacity = capacity_map.get(temple, 5000)
    current_crowd = random.randint(int(capacity * 0.4), capacity)
    status = "Normal"
    if current_crowd > capacity * 0.8:
        status = "High"
    elif current_crowd > capacity * 0.6:
        status = "Moderate"
    return f"📊 Crowd at {temple}: {current_crowd}/{capacity} ({status})."

# --------- Chatbot Responses ----------
def chatbot_response(user_msg):
    intent = get_intent(user_msg)
    temple = match_temple(user_msg)

    if intent == "ask_wait_time":
        if temple:
            return f"⏳ Current wait time is ~45 minutes at {temple}."
        else:
            return "⏳ Current wait times vary by temple. Please specify."

    elif intent == "book_darshan":
        return "✅ Your darshan token is #A123. Slot: 5:30 PM."

    elif intent == "report_emergency":
        return "🚨 Emergency reported! Help will reach immediately."

    elif intent == "get_weather":
        if temple:
            return get_weather(temple)
        else:
            return get_weather()  # default Dwarka

    elif intent == "get_crowd":
        if temple:
            return get_crowd_status(temple)
        else:
            return get_crowd_status()  # default Somnath

    elif intent == "list_temples":
        return "🏯 Available temples: Somnath, Dwarka, Ambaji, Pavagadh.\nYou can ask: 'Weather at Somnath' or 'Crowd in Ambaji'."

    else:
        return "🤖 Sorry, I didn’t understand. You can ask about wait time, booking, emergencies, weather, or crowd."

# --------- Flask Endpoint ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chatbot_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)'''

'''from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random
from fuzzywuzzy import process

app = Flask(__name__)
CORS(app)  # Allow frontend calls

# --------- API Key ----------
WEATHER_API_KEY = "26f2e40b06832ee73c89cd38dc56c64d"  # replace with yours

# --------- Temple Data ----------
temples = ["Somnath", "Dwarka", "Ambaji", "Pavagadh"]
city_map = {
    "Somnath": "Veraval",
    "Dwarka": "Dwarka",
    "Ambaji": "Ambaji",
    "Pavagadh": "Halol"
}
capacity_map = {
    "Somnath": 5000,
    "Dwarka": 4500,
    "Ambaji": 6000,
    "Pavagadh": 4000
}

# --------- Intent Detection ----------
def get_intent(user_msg):
    msg = user_msg.lower()
    if "wait" in msg or "queue" in msg:
        return "ask_wait_time"
    elif "book" in msg or "token" in msg or "darshan" in msg:
        return "book_darshan"
    elif "emergency" in msg or "help" in msg:
        return "report_emergency"
    elif "weather" in msg:
        return "get_weather"
    elif "crowd" in msg:
        return "get_crowd"
    elif "temples" in msg or "options" in msg:
        return "list_temples"
    else:
        return "fallback"

# --------- Fuzzy Temple Matching ----------
def match_temple(user_msg):
    choice, score = process.extractOne(user_msg, temples)
    if score > 70:
        return choice
    return None

# --------- Real-Time API Functions ----------
def get_weather(temple="Dwarka"):
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

def get_crowd_status(temple="Somnath"):
    capacity = capacity_map.get(temple, 5000)
    current_crowd = random.randint(int(capacity * 0.4), capacity)
    status = "Normal"
    if current_crowd > capacity * 0.8:
        status = "High"
    elif current_crowd > capacity * 0.6:
        status = "Moderate"
    return f"📊 Crowd at {temple}: {current_crowd}/{capacity} ({status})."

# --------- Chatbot Responses ----------
def chatbot_response(user_msg):
    intent = get_intent(user_msg)
    temple = match_temple(user_msg)

    if intent == "ask_wait_time":
        if temple:
            return f"⏳ Current wait time is ~45 minutes at {temple}."
        else:
            return "⏳ Current wait times vary by temple. Please specify."

    elif intent == "book_darshan":
        return "✅ Your darshan token is #A123. Slot: 5:30 PM."

    elif intent == "report_emergency":
        return "🚨 Emergency reported! Help will reach immediately."

    elif intent == "get_weather":
        if temple:
            return get_weather(temple)
        else:
            return get_weather()  # default Dwarka

    elif intent == "get_crowd":
        if temple:
            return get_crowd_status(temple)
        else:
            return get_crowd_status()  # default Somnath

    elif intent == "list_temples":
        return "🏯 Available temples: Somnath, Dwarka, Ambaji, Pavagadh.\nYou can ask: 'Weather at Somnath' or 'Crowd in Ambaji'."

    else:
        return "🤖 Sorry, I didn’t understand. You can ask about wait time, booking, emergencies, weather, or crowd."

# --------- Flask Endpoint ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chatbot_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)'''


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)  # allow frontend to call this API

# --------- API Key ----------
WEATHER_API_KEY = "26f2e40b06832ee73c89cd38dc56c64d"  # replace with your key

# --------- Intent Detection ----------
def get_intent(user_msg):
    msg = user_msg.lower()
    if "wait" in msg or "queue" in msg:
        return "ask_wait_time"
    elif "book" in msg or "token" in msg or "darshan" in msg:
        return "book_darshan"
    elif "emergency" in msg or "help" in msg:
        return "report_emergency"
    elif "weather" in msg:
        return "get_weather"
    elif "crowd" in msg:
        return "get_crowd"
    elif "timing" in msg or "open" in msg or "close" in msg or "time" in msg:
        return "get_timings"
    elif "temples" in msg or "options" in msg:
        return "list_temples"
    elif "somnath" in msg or "dwarka" in msg or "ambaji" in msg or "pavagadh" in msg:
        return "temple_info"
    else:
        return "fallback"

# --------- Real-Time API Functions ----------
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

def get_crowd_status(temple="Somnath"):
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
    return f"📊 Crowd at {temple}: {current_crowd}/{capacity} ({status})."

def get_timings(temple="Somnath"):
    timings = {
        "Somnath": "🕑 Somnath Temple: 6:00 AM – 9:00 PM",
        "Dwarka": "🕑 Dwarka Temple: 6:30 AM – 9:30 PM",
        "Ambaji": "🕑 Ambaji Temple: 7:00 AM – 8:30 PM",
        "Pavagadh": "🕑 Pavagadh Temple: 5:00 AM – 7:00 PM"
    }
    return timings.get(temple, "🕑 Temple timings not available.")

def get_temple_info(temple):
    info = {
        "Somnath": "🌊 Somnath Temple: First among the 12 Jyotirlingas, located in Gujarat on the Arabian Sea coast.",
        "Dwarka": "🏝️ Dwarka Temple: Dedicated to Lord Krishna, one of the Char Dham pilgrimage sites.",
        "Ambaji": "🌄 Ambaji Temple: Major Shakti Peetha dedicated to Goddess Amba, in Gujarat.",
        "Pavagadh": "⛰️ Pavagadh Temple: Famous for Maa Kali temple, part of Champaner-Pavagadh UNESCO site."
    }
    return info.get(temple, "ℹ️ No information available.")

# --------- Chatbot Responses ----------
def chatbot_response(user_msg):
    intent = get_intent(user_msg)
    msg = user_msg.lower()

    if intent == "ask_wait_time":
        return "⏳ Current wait time is ~45 minutes at Dwarka."
    elif intent == "book_darshan":
        return "✅ Your darshan token is #A123. Slot: 5:30 PM."
    elif intent == "report_emergency":
        return "🚨 Emergency reported! Help will reach Gate 2 immediately."
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
    elif intent == "get_crowd":
        if "somnath" in msg:
            return get_crowd_status("Somnath")
        elif "dwarka" in msg:
            return get_crowd_status("Dwarka")
        elif "ambaji" in msg:
            return get_crowd_status("Ambaji")
        elif "pavagadh" in msg:
            return get_crowd_status("Pavagadh")
        else:
            return get_crowd_status("Somnath")
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
            return "🕑 Please mention a temple to know timings."
    elif intent == "temple_info":
        if "somnath" in msg:
            return get_temple_info("Somnath")
        elif "dwarka" in msg:
            return get_temple_info("Dwarka")
        elif "ambaji" in msg:
            return get_temple_info("Ambaji")
        elif "pavagadh" in msg:
            return get_temple_info("Pavagadh")
        else:
            return "ℹ️ Please specify a temple name."
    elif intent == "list_temples":
        return "🏯 Available temples: Somnath, Dwarka, Ambaji, Pavagadh.\nYou can ask: 'Weather at Somnath' or 'Crowd in Ambaji'."
    else:
        return "🤖 Sorry, I didn’t understand. You can ask about wait time, booking, emergencies, weather, timings, or crowd."

# --------- Flask Endpoint ----------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    reply = chatbot_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

