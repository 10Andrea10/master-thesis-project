import hashlib
import json
from pytezos.crypto.encoding import base58_decode


def decode_pubkey(pubkey: str) -> bytearray:
    return base58_decode(str.encode(pubkey))

def sha256(lhs: bytearray, rhs: bytearray):
    return hashlib.sha256(lhs + rhs).digest()

def str_to_bytes(point: str, base: int) -> bytearray:
    return int(point, base=base).to_bytes(32, "big", signed=False)

def bytes_to_u_array(val: bytearray, bitsize:int= 32, abi:bool=False) -> list:
    byte_jump = bitsize // 8
    array_arrays = [val[i:i + byte_jump] for i in range(0, len(val), byte_jump)]
    ubit_array = [str(int.from_bytes(x, 'big', signed=False)) for x in array_arrays]
    if abi:
        ubit_array = ["0x" + str(int(x, 16)) for x in ubit_array]
    return ubit_array

def byte32_to_u32_array8(val: bytearray) -> list:
    assert(len(val) == 32)
    return bytes_to_u_array(val)

def decode_signature(signature: str) -> list:
    sig = decode_pubkey(signature)
    return bytes_to_u_array(sig, bitsize=64)

def decode_operation(operation:str) -> list:
    op = bytearray.fromhex(operation[2:])
    return ["0"] + bytes_to_u_array(op, bitsize=64)

def calculate_tree_root(values: [bytearray]) -> bytearray:

    h0 = sha256(values[0], values[1])
    h1 = sha256(values[2], values[3])

    h00 = sha256(h0, h1)

    return byte32_to_u32_array8(h00)

def concatenateTwoArraysIn256(array1: [str], array2: [str]) -> [bytearray]:
    result = []
    for i in range(0, len(array1) ):
        result.append(sha256(str_to_bytes(array1[i], 16), str_to_bytes(array2[i], 16)))
    return result

if __name__ == "__main__":

    # taken from file `dev.env`
    pubkeys = [
        "edpkurPsQ8eUApnLUJ9ZPDvu98E8VNj4KtJa1aZr16Cr5ow5VHKnz4",   # alice
        "edpkvGfYw3LyB1UcCahKQk4rF2tvbMUk8GFiTuMjL75uGXrpvKXhjn",   # bob
        "edpktt6t2ENhxiQqun6bXPPWC6tFVvNPTDRh1gEPGX4BgDgbDnmGzP",   # carlos
        "edpkvS6TDSWcqqj3EJi3NRrCMyN7oNw1B3Hp37R19tMThqM8YNhAuS",   # dave
    ]

    # transactions signatures
    # to generate the operatios in bytes:
    # $  octez-client transfer 1000 from alice to bob -D --burn-cap 0.257 --verbose-signing  
    # to sign the transaction:
    # $  octez-client sign bytes <OPERATION_BYTES> for alice
    transaction_signatures = [
        {
            "operation": "0x08e430e721f59015856d2ddcdc70e4ac36c95b6b24e50b93113056e4a23500396c006b82198cb179e8306c1bedd08f12dc863f328886e10203e907008094ebdc030000a26828841890d3f3a2a1d4083839c7a882fe050100ed59949b798a770ee7ccd88b6202833ab54b3a91758d81645f74d85b981f75e2b79bb864b7924b01dcaab2e0224f09c2607f6db7273fb49f479f9570a26fbb0a",
            "signature": "edsigterWW8Zo4MaL5TnvNNv7eSyUhPm4Zv9ziEj2dgYVeXrETdgEtKr7XmdSxrLYmDSEoXLaptK9pJsgwLm7Wwaebrxox1UQM1",
        },
        {
            "operation": "0x1adcd2f1962fd9dede793cf57598a1976e733f7774838e3d4856fbee95c4e3c46c006b82198cb179e8306c1bedd08f12dc863f328886e10203e907008094ebdc030000e6e6fc837d8fbb6adeec90f7e91b4b4a605386dd00179067c439155181fc9791bfb6e5f1dd049b9f9662869e6379890761c8a10ff5412667e787781c9757aebabc90edf8be71fe29cdd207f28118fcc32d6dec3e07",
            "signature": "edsigu5WKTrVqzoDaZJf1vsjCZ26w1wSFZ2B865GxVujdMWR72qgSgCiekTCr3dKVgvgMvhAPcqWWwwLjRLh1XyR5hVkFXHSGB4",
        },
        {
            "operation": "0x1af6211ad4302d45b8b37987d31f9389851c0a08d511b2c8418e0163d3f30c186c00e6e6fc837d8fbb6adeec90f7e91b4b4a605386dde10201e9070080cab5ee0100006b82198cb179e8306c1bedd08f12dc863f328886002ab73e9c5a9dcb1e4bbf8fc4f99389ed004324b3c9a731d5f0ac22e731d0f9d0d3b313626fd7915907321f25dc6b527b44965cbd67e81fd404367780200bf80e",
            "signature": "edsigtfGjSvaiVoxdGW6wVZQGYvH4CYyV8FsXn5v9uKRnPq9bfUtGw6puA2yWNgjm8Gxwv56orvy4MJ2rrrtbFZa4HKESyfy8Hi",
        },
    ]
    for transaction in transaction_signatures:
        transaction['operation'] = decode_operation(transaction['operation'])
        transaction['signature'] = decode_signature(transaction['signature'])

    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]

    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]

    account_root = calculate_tree_root(decoded_pubkeys)

    balances = [ 
        "0x2DC6C0", # 3000000
        "0x4C4B40", # 5000000
        "0x0",
        "0x0",
    ]

    # balance_root = calculate_tree_root([str_to_bytes(x, 16) for x in balances])

    nonces = [
        "0x2",
        "0x1",
        "0x1",
        "0x1",
    ]

    # nonces_root = calculate_tree_root([str_to_bytes(x, 16) for x in nonces])

    concatenatedBalancesNonces = concatenateTwoArraysIn256(balances, nonces)

    concatenatedBalancesNoncesTreeRoot = calculate_tree_root(concatenatedBalancesNonces)

    transactions = [
        {
            "signature": transaction_signatures[0]['signature'],
            "operation": transaction_signatures[0]['operation'],
	        "amount": "0x3E8", # 1000
            "nonce": "0x3"
        },
        {
            "signature": transaction_signatures[1]['signature'],
            "operation": transaction_signatures[1]['operation'],
	        "amount": "0x3E8",
            "nonce": "0x2"
        },
        {
            "signature": transaction_signatures[2]['signature'],
            "operation": transaction_signatures[2]['operation'],
	        "amount": "0x1F4", # 500
            "nonce": "0x4"
        },
    ]

    transaction_extras = [
        {
	        "sourceAddress": formatted_accounts[0],
            "targetAddress": formatted_accounts[1],
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
        },
        {
	        "sourceAddress": formatted_accounts[1],
            "targetAddress": formatted_accounts[2],
            "sourceIndex": "0x1",
            "targetIndex": "0x2",
        },
        {
	        "sourceAddress":  formatted_accounts[0],
            "targetAddress":  formatted_accounts[1],
            "sourceIndex": "0x0",
            "targetIndex": "0x1",
        },
    ]


    obj = json.dumps([
        account_root,
        formatted_accounts,
        #balance_root,
        concatenatedBalancesNoncesTreeRoot,
        balances,
        # nonces_root,
        nonces,
        transactions,
        transaction_extras
    ], indent=4)

    with open("sampleZokinput.json", "w") as outfile:
        outfile.write(obj)
