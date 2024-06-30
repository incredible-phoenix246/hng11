#!/usr/bin/python3
"""
A basic Flask web server that provides an API endpoint to greet visitors
and returns their IP address and location.

API Endpoint:
    GET /api/hello?visitor_name=<name>

Response:
    {
        "client_ip": "<IP address of the requester>",
        "location": {
            "city": "<City of the requester>",
            "region": "<Region of the requester>",
            "country": "<Country of the requester>"
        },
        "greeting": "Hello, <name>!"
    }
"""

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the IPINFO token from the environment variables
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')

app = Flask(__name__)

def get_location(ip):
    """
    Get the location of the IP address using the ipinfo.io API.

    Args:
        ip (str): The IP address of the requester.

    Returns:
        dict: A dictionary containing the city, region, and country corresponding to the IP address,
              or "Unknown" if unable to fetch.
    """
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}')
        data = response.json()
        return {
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown')
        }
    except Exception as e:
        print(f'Error fetching location: {e}')
        return {'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown'}


@app.route('/', methods=['GET'])
def hello_world():
    """
    Handle GET requests to the root URL.

    Returns:
        str: A simple "Hello, World!" message.
    """
    return "Hello, World!"

@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Handle GET requests to the /api/hello endpoint.

    Query Parameters:
        visitor_name (str): The name of the visitor (optional).

    Returns:
        JSON: A JSON response containing the client's IP address, public IP address of the server,
              location, and a greeting message.
    """
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr
    location = get_location(client_ip)
    formatted_location = f"{location['city']}, {location['country']}"
    
    response = {
        "client_ip": client_ip,
        "location": formatted_location,
        "greeting": f"Hello, {visitor_name}!"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
