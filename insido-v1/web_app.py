from flask import Flask, request, jsonify, send_from_directory, session
from insido_engine import ask_insido
import uuid, time

app = Flask(__name__)
app.secret_key = "insido-final-secret"

# visitor_id -> last_seen_time
online_users = {}

@app.before_request
def track_online():
    now = time.time()
    if "vid" not in session:
        session["vid"] = str(uuid.uuid4())
    online_users[session["vid"]] = now

    # remove inactive users (30 seconds)
    for vid in list(online_users.keys()):
        if now - online_users[vid] > 30:
            del online_users[vid]

@app.route("/")
def index():
    return send_from_directory(".", "ui.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": ""})

    reply = ask_insido(message)
    return jsonify({"reply": reply})

@app.route("/online")
def online():
    return jsonify({"count": len(online_users)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
