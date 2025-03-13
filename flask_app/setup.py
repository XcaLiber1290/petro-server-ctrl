import json
import os

def create_config():
    print("Welcome to the setup process! Please provide the following details:")

    # Collecting user input
    app_id = input("Enter your unique App ID: ")
    panel_url = input("Enter your Pterodactyl Panel URL (e.g., https://your-pterodactyl-panel.com): ")
    api_key = input("Enter your Pterodactyl API Key: ")
    server_id = input("Enter your Pterodactyl Server ID: ")
    server_address = input("Enter your Minecraft Server IP/Domain (e.g., your.server.ip or your.server.com): ")

    # Create a config.json file with the provided details
    config_data = {
        "app_id": app_id,
        "panel_url": panel_url,
        "api_key": api_key,
        "server_id": server_id,
        "server_address": server_address
    }

    config_path = os.path.join(os.getcwd(), "config.json")

    # Check if config.json already exists
    if os.path.exists(config_path):
        print(f"{config_path} already exists. Overwriting it with new details.")
    
    # Writing the configuration to a file
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    
    print(f"config.json created successfully at {config_path}")

def main():
    create_config()

if __name__ == "__main__":
    main()
