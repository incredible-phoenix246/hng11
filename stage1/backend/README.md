# Flask API for Greeting Visitors

This is a basic Flask web server that provides an API endpoint to greet visitors and returns their IP address and location.

## API Endpoint

- **Endpoint**: `/api/hello`
- **Method**: `GET`
- **Query Parameters**:
  - `visitor_name` (optional): The name of the visitor. If not provided, the default is "Guest".

### Example Request

```curl
    GET /api/hello?visitor_name=Phoenix
```

### Example Response

```json
{
  "client_ip": "127.0.0.1",
  "location": {
    "city": "New York",
    "region": "New York",
    "country": "US"
  },
  "greeting": "Hello, Phoenix!"
}
```

### Installation

- **Clone the repository:**

```bash
    git clone https://github.com/incredible-phoenix246/hng11
    cd hng11/stage1/backend
```

- **Create a virtual environment and activate it:**

```python
    python3 -m venv venv
    source venv/bin/activate
```

- **Install the dependencies:**

```python
    pip install -r requirements.txt
```

- **Create a `.env`**

```bash
    IPINFO_TOKEN=your_ipinfo_token
```

- **Run The Application**
  To run the application locally:

```python
    python app.py
```
