#!/usr/bin/python3
"""
A basic FastAPI web server that provides an API endpoint to greet visitors,
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

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

app = FastAPI()


def get_weather_info(ip: str) -> dict:
    """
    Get the weather information and location for a given IP address using the WeatherAPI.

    Args:
        ip (str): The IP address of the requester.

    Returns:
        dict: A dictionary containing the city, country, and temperature in Celsius.
    """
    try:
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={ip}&aqi=no')
        data = response.json()
        location = data['location']
        current = data['current']
        return {
            'city': location['name'],
            'country': location['country'],
            'temperature': current['temp_c']
        }
    except Exception as e:
        print(f'Error fetching weather information: {e}')
        return {'city': 'Unknown', 'country': 'Unknown', 'temperature': 'Unknown'}


@app.get('/')
async def hello_world():
    """
    Handle GET requests to the root URL.

    Returns:
        str: A simple "Hello, World!" message.
    """
    return "Hello, World!"


@app.get('/api/hello')
async def hello(request: Request, visitor_name: str = "Guest"):
    """
    Handle GET requests to the /api/hello endpoint.

    Query Parameters:
        visitor_name (str): The name of the visitor (optional).

    Returns:
        JSON: A JSON response containing the client's IP address, location,
              temperature, and a greeting message.
    """
    client_ip = request.client.host
    weather_info = get_weather_info(client_ip)

    city = weather_info['city']
    country = weather_info['country']
    temperature = weather_info['temperature']
    formatted_location = f"{city}, {country}"
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": formatted_location,
        "greeting": greeting
    }
    return JSONResponse(content=response)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
