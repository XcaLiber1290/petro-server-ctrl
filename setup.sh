#!/bin/bash
echo "Enter your Pterodactyl Panel URL: "
read PANEL_URL
echo "Enter your API Key: "
read API_KEY
echo "Enter your Server ID: "
read SERVER_ID

cat <<EOL > backend/config.json
{
    "PANEL_URL": "$PANEL_URL",
    "API_KEY": "$API_KEY",
    "SERVER_ID": "$SERVER_ID"
}
EOL

echo "Configuration saved to backend/config.json"