import requests

BASE_URL = "http://localhost:3000"


def execute_deposit(signer_key):
    """Execute the deposit queue"""

    payload = {
        "privateSignerKey": signer_key,
    }

    url = f"{BASE_URL}/deposit"
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Deposit executed successfully!")
        return response
    else:
        raise Exception(f"Error: {response.status_code} in execute deposit")

def withdraw(signer_key, position, amount, signature):
    payload = {
        "privateSignerKey": signer_key,
        "position": position,
        "amount": amount,
        "signature": signature
    }
    url = f"{BASE_URL}/withdraw"
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Withdraw executed successfully!")
    else:
        raise Exception(f"Error: {response.status_code} in withdraw")
        