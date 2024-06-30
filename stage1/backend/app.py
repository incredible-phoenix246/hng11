#!/usr/bin/python3
"""
A basic Flask web server that provides an API endpoint to greet visitors,
returns their IP address, location, and current temperature.

API Endpoint:
    GET /api/hello?visitor_name=<name>

Response:
    {
        "client_ip": "<IP address of the requester>",
        "location": "<City, Country of the requester>",
        "greeting": "Hello, <name>!, the temperature is <temperature> degrees Celsius in <City>"
    }
"""

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the IPINFO token and OpenWeatherMap API key from the environment variables
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

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

def get_temperature(city):
    """
    Get the current temperature for a given city using the OpenWeatherMap API.

    Args:
        city (str): The name of the city.

    Returns:
        float: The current temperature in Celsius.
    """
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}')
        data = response.json()
        return data['main']['temp']
    except Exception as e:
        print(f'Error fetching temperature: {e}')
        return None

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
        JSON: A JSON response containing the client's IP address, location,
              temperature, and a greeting message.
    """
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr
    location = get_location(client_ip)
    city = location['city']
    temperature = get_temperature(city)

    formatted_location = f"{city}, {location['country']}"
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": formatted_location,
        "greeting": greeting
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
