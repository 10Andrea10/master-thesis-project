import json


if __name__ == "__main__":
    
    num_transactions = 1024
    transactions = []

    transactions.append({"sourceIndex": "0x1", "targetIndex": "0x2",
                         "amount": "0x3E8", "nonce": "0x2"})

    for i in range(1, num_transactions):
        transaction = {
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
            "amount": "0x3E8",  # 1000
            "nonce": f"{hex(i+1)}",
        }
        transactions.append(transaction)
    
    obj = json.dumps(
        [
            transactions
        ],
        indent=4,
    )
    file_name = f"transactions-plain.json"

    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)
