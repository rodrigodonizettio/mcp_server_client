# Create project directory
uv init weather-client
cd weather-client

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install required packages
uv add mcp anthropic python-dotenv boto3

# Remove boilerplate files
rm main.py

# Create our main file
touch weather_client.py
