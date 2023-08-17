import json

if __name__ == "__main__":
    num_users = 2048

    # Generate initial data
    balances = ["0x0" for _ in range(num_users)]
    balances[0] = "0x3000000"  # First user balance
    balances[1] = "0x5000000"  # Second user balance

    nonces = ["0x0" for _ in range(num_users)]
    nonces[0] = "0x1"  # First user nonce
    nonces[1] = "0x1"  # Second user nonce

    obj = json.dumps(
        [
            balances,
            nonces,
        ],
        indent=4,
    )
    
    file_name = f"balances-nonces-list-{num_users}.json"
    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)