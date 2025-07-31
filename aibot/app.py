import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)  # ✅ No need to set template/static paths manually

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    model = data.get("model", "gpt-3.5-turbo")

    if not API_KEY:
        return jsonify({"message": "⚠️ API key not configured on server."}), 500

    if not user_msg:
        return jsonify({"message": "Please enter a message."})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        result = resp.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not reply:
            reply = "⚠️ No reply from model."
    except requests.exceptions.RequestException as e:
        print("API Request Error:", e)
        reply = "⚠️ Problem connecting to the API."
    except Exception as e:
        print("Server Error:", e)
        reply = "❌ Server error."

    return jsonify({"message": reply})
