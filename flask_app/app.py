from flask import Flask, jsonify, render_template, request
import json
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load configuration from config.json
def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("config.json not found. Please run the setup script first.")
        exit()

# Load config
config = load_config()

PANEL_API_URL = config["panel_url"]
API_KEY = config["api_key"]
SERVER_ID = config["server_id"]
SERVER_ADDRESS = config["server_address"]

# Set the headers for Pterodactyl API
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Function to call Pterodactyl API
def pterodactyl_api_request(endpoint, method="GET", data=None):
    # Make sure we're using the correct API endpoint structure
    if not PANEL_API_URL.endswith('/api'):
        url = f"{PANEL_API_URL}/api/{endpoint}"
    else:
        url = f"{PANEL_API_URL}/{endpoint}"
    
    logging.info(f"Making {method} request to: {url}")
    if data:
        logging.info(f"Request data: {data}")
    
    try:
        response = requests.request(method, url, headers=HEADERS, json=data, timeout=10)
        
        # Log the response for debugging
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content length: {len(response.text)}")
        
        # Check if the response status code is successful (200-299)
        if response.status_code >= 200 and response.status_code < 300:
            # For power actions, a 204 No Content response is common and valid
            if response.status_code == 204 or not response.text.strip():
                return {"success": True, "message": f"{method} operation completed successfully"}
            
            try:
                return response.json()  # Try parsing the response as JSON
            except requests.exceptions.JSONDecodeError:
                logging.error(f"Failed to parse JSON from response: {response.text}")
                # Return success anyway if status code was successful
                if response.status_code < 300:
                    return {"success": True, "message": "Operation completed successfully", "raw_response": response.text[:100]}
                return {"error": "Failed to parse JSON response"}
        else:
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            return {"error": f"API request failed with status {response.status_code}", "details": response.text}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {"error": f"Request failed: {str(e)}"}

# Get server status and player count from Pterodactyl and mcstatus.io
# Get server status from Pterodactyl and mcstatus.io
def get_server_status():
    # Fetch server data from Pterodactyl API
    server_data = pterodactyl_api_request(f"client/servers/{SERVER_ID}/resources")
    if not server_data or "error" in server_data:
        logging.error(f"Failed to get server status: {server_data}")
        return {"online": False, "players_online": 0, "uptime": 0}

    # Check for attributes in both standard response and attributes
    if "attributes" in server_data:
        attributes = server_data["attributes"]
    else:
        attributes = server_data
    
    online_status = attributes.get("current_state", "offline") == "running"
    uptime = attributes.get("resources", {}).get("uptime", 0)  # In seconds
    
    # Get player count from mcstatus.io API
    player_count = get_player_count_from_mcstatus()

    return {
        "online": online_status,
        "players_online": player_count,
        "uptime": uptime  # Return uptime in seconds
    }

# Get player count from mcstatus.io
def get_player_count_from_mcstatus():
    url = f"https://api.mcstatus.io/v2/status/java/{SERVER_ADDRESS}"
    try:
        response = requests.get(url, timeout=5)
        status_data = response.json()
        return status_data.get("players", {}).get("online", 0)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching player count: {e}")
        return 0

@app.route('/')
def index():
    # Get the server status and player count
    status = get_server_status()
    player_count = status.get("players_online", 0)
    online_status = status.get("online", False)
    uptime = status.get("uptime", "N/A")

    return render_template('index.html', status=online_status, player_count=player_count, uptime=uptime)

# Server power endpoints
@app.route('/api/server-status', methods=['GET'])
def api_server_status():
    return jsonify(get_server_status())

# Start the server
@app.route('/start-server', methods=['POST'])
def start_server():
    response = pterodactyl_api_request(f"client/servers/{SERVER_ID}/power", "POST", {"signal": "start"})
    return jsonify(response)

# Stop the server
@app.route('/stop-server', methods=['POST'])
def stop_server():
    response = pterodactyl_api_request(f"client/servers/{SERVER_ID}/power", "POST", {"signal": "stop"})
    return jsonify(response)

# Restart the server
@app.route('/restart-server', methods=['POST'])
def restart_server():
    response = pterodactyl_api_request(f"client/servers/{SERVER_ID}/power", "POST", {"signal": "restart"})
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)