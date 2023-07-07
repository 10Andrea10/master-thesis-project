import hashlib
import json
from pytezos.crypto.encoding import base58_decode


def decode_pubkey(pubkey: str) -> bytearray:
    if pubkey == "":
        # create a bitearray of length 32 filled with 0s
        return bytearray(32)
    return base58_decode(str.encode(pubkey))


def sha256(lhs: bytearray, rhs: bytearray):
    return hashlib.sha256(lhs + rhs).digest()


def str_to_bytes(point: str, base: int) -> bytes:
    return int(point, base=base).to_bytes(32, "big", signed=False)


def bytes_to_u_array(val: bytearray, bitsize: int = 32, abi: bool = False) -> list:
    byte_jump = bitsize // 8
    array_arrays = [val[i:i + byte_jump]
                    for i in range(0, len(val), byte_jump)]
    ubit_array = [str(int.from_bytes(x, 'big', signed=False))
                  for x in array_arrays]
    if abi:
        ubit_array = ["0x" + str(int(x, 16)) for x in ubit_array]
    return ubit_array


def byte32_to_u32_array8(val: bytearray) -> list:
    if val == b"":
        fake_array = bytearray(32)
        return bytes_to_u_array(fake_array)

    assert (len(val) == 32)
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
        result.append(
            sha256(str_to_bytes(array1[i], 16), str_to_bytes(array2[i], 16)))
    return result


if __name__ == "__main__":

    # taken from file `dev.env`
    pubkeys = [
        "edpkurPsQ8eUApnLUJ9ZPDvu98E8VNj4KtJa1aZr16Cr5ow5VHKnz4",   # alice
        "edpkvGfYw3LyB1UcCahKQk4rF2tvbMUk8GFiTuMjL75uGXrpvKXhjn",   # bob
        "",   # deregistered
        "edpkvS6TDSWcqqj3EJi3NRrCMyN7oNw1B3Hp37R19tMThqM8YNhAuS",   # jane
    ]

    newUser = "edpkuT1QYPYbLLQz9dXhQS33ncsixxeGHbNGmntPTR4VBbWmskHPrV" # joe
    newUserDecoded = decode_pubkey(newUser)
    newuserFormatted = byte32_to_u32_array8(newUserDecoded)

    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]

    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]

    account_root = calculate_tree_root(decoded_pubkeys)

    balances = [
        "0x2DC6C0",  # 3000000
        "0x4C4B40",  # 5000000
        "0x0",
        "0x0",
    ]

    # balance_root = calculate_tree_root([str_to_bytes(x, 16) for x in balances])

    # NOTE: the nonce for the deregistered one is 0. Future use.
    nonces = [
        "0x1",
        "0x1",
        "0x0",
        "0x1",
    ]

    # nonces_root = calculate_tree_root([str_to_bytes(x, 16) for x in nonces])

    # NOTE: this signature is a fake, not yet checked in the middleware
    signature = "edsigterWW8Zo4MaL5TnvNNv7eSyUhPm4Zv9ziEj2dgYVeXrETdgEtKr7XmdSxrLYmDSEoXLaptK9pJsgwLm7Wwaebrxox1UQM1"
    decoded_signature = decode_signature(signature)


    concatenatedBalancesNonces = concatenate_two_arrays_in_256(balances, nonces)

    concatenatedBalancesNoncesTreeRoot = calculate_tree_root(
        concatenatedBalancesNonces)

    obj = json.dumps([
        account_root,
        formatted_accounts,
        concatenatedBalancesNoncesTreeRoot,
        balances,
        nonces,
        "0x2",
        newuserFormatted,
        decoded_signature
    ], indent=4)

    with open("sampleZokinput.json", "w") as outfile:
        outfile.write(obj)
