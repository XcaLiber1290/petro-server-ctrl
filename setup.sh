#!/bin/bash

# Create project folder
echo "Creating project folder..."
mkdir flask_app
cd flask_app

# Create subdirectories for static files and templates
echo "Creating directories..."
mkdir -p static/css static/js templates

# Create app.py
echo "Creating app.py..."
cat <<EOL > app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create index.html template
echo "Creating index.html..."
cat <<EOL > templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Welcome to the Flask App!</h1>
    <button id="action-btn">Click Me</button>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
EOL

# Create CSS file
echo "Creating style.css..."
cat <<EOL > static/css/style.css
body {
    font-family: Arial, sans-serif;
    background-color: #2d2d2d;
    color: white;
    text-align: center;
    padding: 20px;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
EOL

# Create JavaScript file
echo "Creating script.js..."
cat <<EOL > static/js/script.js
document.getElementById('action-btn').addEventListener('click', function() {
    alert('Button clicked!');
});
EOL

# Create setup.sh script
echo "Creating setup.sh..."
cat <<EOL > setup.sh
#!/bin/bash

# Update system and install dependencies
echo "Updating system..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and pip
echo "Installing Python and pip..."
sudo apt-get install python3 python3-pip -y

# Install Flask using pip
echo "Installing Flask..."
pip3 install flask

# Create virtual environment (optional)
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies (optional)
echo "Installing dependencies in virtual environment..."
pip install -r requirements.txt

# Provide instructions
echo "Setup complete!"
echo "To run the app, use the following commands:"
echo "1. Source the virtual environment: source venv/bin/activate"
echo "2. Run the Flask app: python app.py"
EOL

# Create requirements.txt file
echo "Creating requirements.txt..."
cat <<EOL > requirements.txt
Flask==2.1.0
EOL

# Provide completion message
echo "Flask app structure created successfully!"
echo "Run ./setup.sh to install dependencies and set up the environment."
