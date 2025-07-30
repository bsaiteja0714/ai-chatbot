import os, json, requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # loads OPENROUTER_API_KEY

app = Flask(__name__)
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def log_history(role, content):
    # Optionally write to a file or database here
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data        = request.get_json()
    user_msg    = data.get("message", "").strip()
    model       = data.get("model", "gpt-3.5-turbo")
    if not user_msg:
        return jsonify({"message": "Please enter a message."})

    # You can also log_history("user", user_msg)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        result  = resp.json()
        choices = result.get("choices", [])
        if choices and "message" in choices[0]:
            reply = choices[0]["message"]["content"].strip()
        else:
            reply = "⚠️ No reply."
        # log_history("assistant", reply)
    except requests.exceptions.HTTPError:
        print("HTTP Error:", resp.text)
        reply = "⚠️ HTTP error from API."
    except Exception as e:
        print("Error:", e)
        reply = "❌ Server error."

    return jsonify({"message": reply})

if __name__ == "__main__":
    app.run(debug=True)
app = app  # Required for gunicorn to recognize it




