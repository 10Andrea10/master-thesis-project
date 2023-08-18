import json
from utils import decode_pubkey, byte32_to_u32_array8

if __name__ == "__main__":
    num_users = 256
    num_transactions = 50

    # Generate initial data
    pubkeys = [
        "edpku3EDFkXF2MHSipDKF2caz85yondEgqrohxdPdpXRpiX2tkFzuY",  # bob
        "edpkunwYWwaUUGPtbTGmggBB1dgmj5Ly8F9CwYHRL99XEDUgskgNBK",  # alice
        "edpkvRCLKPFrg7eYXLsKLjjZqYnsVtoZdRtF4RyzLzRFMHsqFrxpFF",  # john
        "edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH",  # jane
    ]
    
    for _ in range(num_users - 4 ):
        pubkeys.append("edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH")

    with open('./output_files/signatures.json') as json_file:
        signatures = json.load(json_file)

    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]
    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]
    # account_root = calculate_tree_root(decoded_pubkeys)
    # account_root_poseidon = calculate_tree_root_zok(decoded_pubkeys)

    account_root = "0x7A3312C13C04789D3CEB9D22E23CF17ADA834CC8C7C25FEFCB6507291DB8708"
    concatenatedBalancesNoncesTreeRoot = "0x4C1E922AC466B7D04713FBF2C4A9F1F8E2F03BEE75C0DFF4532EF5C56EB54DCA"

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

    # concatenatedBalancesNonces = concatenate_two_arrays_in_256(
    #     balances, nonces)
    # concatenatedBalancesNoncesTreeRoot = calculate_tree_root(
    #     concatenatedBalancesNonces)

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
