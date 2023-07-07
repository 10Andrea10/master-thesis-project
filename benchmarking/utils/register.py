import requests

# Define the base URL of the REST API
BASE_URL = "http://localhost:3000"

# Make aput request to register the user

# Make a POST request to send data to the server
def send_register(signer_key, position, user_public_key, signature):
    """ Register the user 

    Args:
        signer_key (_type_): key of the signer
        position (_type_): _description_
        user_public_key (_type_): _description_
        signature (_type_): _description_
    """
    url = f"{BASE_URL}/user"
    data = {
        "privateSignerKey": signer_key,
        "position": position,
        "userPublicKey": user_public_key,
        "signature": signature
    }
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print("Register sent successfully!")
    else:
        print(f"Error {response.status_code} in register")
