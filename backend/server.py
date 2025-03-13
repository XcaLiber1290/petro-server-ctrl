from flask import Flask, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__)
CONFIG_PATH = "config.json"

# Load configuration
def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)

@app.route("/status", methods=["GET"])
def get_status():
    config = load_config()
    headers = {"Authorization": f"Bearer {config['API_KEY']}", "Accept": "application/json"}
    url = f"{config['PANEL_URL']}/api/client/servers/{config['SERVER_ID']}"
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route("/action", methods=["POST"])
def server_action():
    config = load_config()
    data = request.json
    headers = {"Authorization": f"Bearer {config['API_KEY']}", "Accept": "application/json"}
    url = f"{config['PANEL_URL']}/api/client/servers/{config['SERVER_ID']}/power"
    response = requests.post(url, json={"signal": data["action"]}, headers=headers)
    return jsonify(response.json())

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

