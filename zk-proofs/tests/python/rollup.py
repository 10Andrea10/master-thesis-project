import json
from utils import decode_pubkey, calculate_tree_root, concatenate_two_arrays_in_256, byte32_to_u32_array8

if __name__ == "__main__":
    num_users = 4
    num_transactions = 30

    # Generate initial data
    pubkeys = [
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4" for _ in range(num_users)
    ]
    pubkeys[3] = ""
    
    file_path = './output_files/zokrate-signature-input-ramon-50.json'

    with open(file_path, 'r') as file:
        data = json.load(file) # 0, 1, 1000, 1 + i
    
    signatures = [
        { # 1, 2, 1000, 2
            "r": [
                "12208776621866386368519600434257825921555383783020262696401561725161443218565",
                "42099659853764012415077786415304351648740015586463863995849451685412124172850"
            ],
            "s": "2098404967612575486283620368662466401991716185579121887552944125596937539059",
            "a": [
                "9463778183056102078866993118044984671658132484107251542179921426381620273800",
                "4635611125295530335317425380928224173124053237108412540578596412445271041431"
            ]
        }
    ]
    
    signatures.extend(data)
    
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
        "signature": signatures[0]})

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
            "signature": signatures[i],
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
    
    file_name = f"rollup-{num_users}-{num_transactions}-inputs.json"

    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)
