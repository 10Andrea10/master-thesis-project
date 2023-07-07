import requests

BASE_URL = "http://localhost:3000"


def sign_register(private_key, position, user_public_key):
    """Sign the register request"""
    
    # Create the payload
    payload = {
        "privateSignerKey": private_key,
        "position": position,
        "userPublicKey": user_public_key
    }
    
    url = f"{BASE_URL}/sign/register"
    response = requests.get(url, json=payload, timeout = 5000)
    if  response.status_code == 200:
        print("Register signed successfully!")
        return response
    else:
        print(f"Error: {response.status_code} in sing register")
    