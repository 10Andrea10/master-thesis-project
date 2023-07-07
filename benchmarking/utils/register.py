import requests

# Define the base URL of the REST API
base_url = "localhost:3000"

# Make aput request to register the user

# Make a POST request to send data to the server
def send_register(data):
    url = f"{base_url}/user"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print("Register sent successfully!")
    else:
        print(f"Error: {response.status_code}")
