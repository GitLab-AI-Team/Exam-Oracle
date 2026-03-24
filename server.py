from flask import Flask, request, jsonify
from app.webhook_handler import handle_webhook

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({"error": "invalid or missing JSON payload"}), 400

    result = handle_webhook(payload)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
    