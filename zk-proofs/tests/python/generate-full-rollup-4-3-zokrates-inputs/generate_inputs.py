import hashlib
import json
from pytezos.crypto.encoding import base58_decode


def decode_pubkey(pubkey: str) -> bytearray:
    return base58_decode(str.encode(pubkey))


def sha256(lhs: bytearray, rhs: bytearray):
    return hashlib.sha256(lhs + rhs).digest()


def str_to_bytes(point: str, base: int) -> bytes:
    return int(point, base=base).to_bytes(32, "big", signed=False)


def bytes_to_u_array(val: bytearray, bitsize: int = 32, abi: bool = False) -> list:
    byte_jump = bitsize // 8
    array_arrays = [val[i : i + byte_jump] for i in range(0, len(val), byte_jump)]
    ubit_array = [str(int.from_bytes(x, "big", signed=False)) for x in array_arrays]
    if abi:
        ubit_array = ["0x" + str(int(x, 16)) for x in ubit_array]
    return ubit_array


def byte32_to_u32_array8(val: bytearray) -> list:
    assert len(val) == 32
    return bytes_to_u_array(val)


def decode_signature(signature: str) -> list:
    sig = decode_pubkey(signature)
    return bytes_to_u_array(sig, bitsize=64)


def decode_operation(operation: str) -> list:
    op = bytearray.fromhex(operation[2:])
    return ["0"] + bytes_to_u_array(op, bitsize=64)


def calculate_tree_root(values: [bytearray]) -> bytearray:
    h0 = sha256(values[0], values[1])
    h1 = sha256(values[2], values[3])

    h00 = sha256(h0, h1)

    return byte32_to_u32_array8(h00)


def concatenate_two_arrays_in_256(array1: [str], array2: [str]) -> [bytearray]:
    result = []
    for i in range(0, len(array1)):
        result.append(sha256(str_to_bytes(array1[i], 16), str_to_bytes(array2[i], 16)))
    return result


if __name__ == "__main__":
    pubkeys = [
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
        "edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4",
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
    ]

    # balance_root = calculate_tree_root([str_to_bytes(x, 16) for x in balances])

    nonces = [
        "0x1",
        "0x1",
        "0x0",
        "0x0",
    ]

    # nonces_root = calculate_tree_root([str_to_bytes(x, 16) for x in nonces])

    concatenatedBalancesNonces = concatenate_two_arrays_in_256(balances, nonces)

    concatenatedBalancesNoncesTreeRoot = calculate_tree_root(concatenatedBalancesNonces)

    transactions = [
        {
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
            "amount": "0x3E8",  # 1000
            "nonce": "0x2",
        },
        {"sourceIndex": "0x1", "targetIndex": "0x2", "amount": "0x3E8", "nonce": "0x2"},
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

    with open("sampleZokinput.json", "w") as outfile:
        outfile.write(obj)
