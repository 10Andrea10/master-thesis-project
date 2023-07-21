import json

from test_utils import decode_signature, decode_pubkey, calculate_tree_root, concatenate_two_arrays_in_256, byte32_to_u32_array8

if __name__ == "__main__":
    pubkeys = [
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
    ]

    # transactions signatures
    # to generate the operatios in bytes:
    # $  octez-client transfer 1000 from alice to bob -D --burn-cap 0.257 --verbose-signing
    # to sign the transaction:
    # $  octez-client sign bytes <OPERATION_BYTES> for alice
    signatures = [
        "edsigterWW8Zo4MaL5TnvNNv7eSyUhPm4Zv9ziEj2dgYVeXrETdgEtKr7XmdSxrLYmDSEoXLaptK9pJsgwLm7Wwaebrxox1UQM1",
        "edsigu5WKTrVqzoDaZJf1vsjCZ26w1wSFZ2B865GxVujdMWR72qgSgCiekTCr3dKVgvgMvhAPcqWWwwLjRLh1XyR5hVkFXHSGB4",
        "edsigtfGjSvaiVoxdGW6wVZQGYvH4CYyV8FsXn5v9uKRnPq9bfUtGw6puA2yWNgjm8Gxwv56orvy4MJ2rrrtbFZa4HKESyfy8Hi",
    ]
    decoded_signatures = []
    for signature in signatures:
        decoded_signatures.append(decode_signature(signature))

    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]

    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]

    account_root = calculate_tree_root(decoded_pubkeys)

    balances = [
        "0x3000000",  # 3000000
        "0x5000000",  # 5000000
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x3000000",  # 3000000
        "0x5000000",  # 5000000
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",

    ]

    # balance_root = calculate_tree_root([str_to_bytes(x, 16) for x in balances])

    nonces = [
        "0x1",
        "0x1",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x1",
        "0x1",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
        "0x0",
    ]

    # nonces_root = calculate_tree_root([str_to_bytes(x, 16) for x in nonces])

    concatenatedBalancesNonces = concatenate_two_arrays_in_256(
        balances, nonces)

    concatenatedBalancesNoncesTreeRoot = calculate_tree_root(
        concatenatedBalancesNonces)

    transactions = [
        {
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
            "amount": "0x3E8",  # 1000
            "nonce": "0x2",
        },
        {"sourceIndex": "0x1", "targetIndex": "0x2",
            "amount": "0x3E8", "nonce": "0x2"},
        {
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
            "amount": "0x1F4",  # 500
            "nonce": "0x3",
        },
    ]

    transaction_extras = [
        {
            "sourceAddress": formatted_accounts[0],
            "targetAddress": formatted_accounts[1],
            "signature": decoded_signatures[0],
        },
        {
            "sourceAddress": formatted_accounts[1],
            "targetAddress": formatted_accounts[2],
            "signature": decoded_signatures[1],
        },
        {
            "sourceAddress": formatted_accounts[0],
            "targetAddress": formatted_accounts[1],
            "signature": decoded_signatures[2],
        },
    ]

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

    with open("output_files/rollup-16-3-inputs.json", "w") as outfile:
        outfile.write(obj)
