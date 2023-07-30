import json
from test_utils import decode_signature, decode_pubkey, calculate_tree_root, concatenate_two_arrays_in_256, byte32_to_u32_array8

if __name__ == "__main__":
    num_users = 4
    num_transactions = 50

    # Generate initial data
    pubkeys = [
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4" for _ in range(num_users)
    ]
    pubkeys[3] = ""
    signatures = [
        "edsigtfGjSvaiVoxdGW6wVZQGYvH4CYyV8FsXn5v9uKRnPq9bfUtGw6puA2yWNgjm8Gxwv56orvy4MJ2rrrtbFZa4HKESyfy8Hi" for _ in range(num_transactions)
    ]
    decoded_signatures = [decode_signature(
        signature) for signature in signatures]
    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]
    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]
    account_root = calculate_tree_root(decoded_pubkeys)

    # Generate balances and nonces
    balances = ["0x0" for _ in range(num_users)]
    balances[0] = "0x3000000"  # First user balance
    balances[1] = "0x5000000"  # Second user balance

    nonces = ["0x0" for _ in range(num_users)]
    nonces[0] = "0x1"  # First user nonce
    nonces[1] = "0x1"  # Second user nonce

    # Generate transactions
    transactions = []
    transaction_extras = []

    transactions.append({"sourceIndex": "0x1", "targetIndex": "0x2",
                         "amount": "0x3E8", "nonce": "0x2"})
    transaction_extras.append({
        "sourceAddress": formatted_accounts[1],
        "targetAddress": formatted_accounts[2],
        "signature": decoded_signatures[0]})

    for i in range(1, num_transactions):
        transaction = {
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
            "amount": "0x3E8",  # 1000
            "nonce": f"{hex(i+1)}",
        }
        transactions.append(transaction)

        transaction_extra = {
            "sourceAddress": formatted_accounts[0],
            "targetAddress": formatted_accounts[1],
            "signature": decoded_signatures[i],
        }
        transaction_extras.append(transaction_extra)

    concatenatedBalancesNonces = concatenate_two_arrays_in_256(
        balances, nonces)
    concatenatedBalancesNoncesTreeRoot = calculate_tree_root(
        concatenatedBalancesNonces)

    # Create and write to JSON file
    obj = json.dumps(
        [
            account_root,
            formatted_accounts,
            concatenatedBalancesNoncesTreeRoot,
            balances,
            nonces,
            transactions,
            transaction_extras,
        ],
        indent=4,
    )
    
    file_name = f"rollup-{num_users}-{num_transactions}-noSig-inputs.json"

    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)
