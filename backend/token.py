import requests
import os

data = {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
}

response = requests.post('http://localhost:9090/o/token/', data=data)
print(response.json())
