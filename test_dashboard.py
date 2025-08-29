import requests

try:
    response = requests.get('http://127.0.0.1:8000/api/spendings/dashboard')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Dashboard API is working!")
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error connecting to dashboard: {e}")
