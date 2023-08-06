from hashlib import sha3_256 as sha_ext
from typing import List
from pytezos.crypto.encoding import base58_decode

def decode_pubkey(pubkey: str) -> bytearray:
    if pubkey == "":
        # create a bitearray of length 32 filled with 0s
        return bytearray(32)
    return base58_decode(str.encode(pubkey))


def sha256(lhs: bytearray, rhs: bytearray):
    return sha_ext(lhs + rhs).digest()


def str_to_bytes(point: str, base: int) -> bytes:
    return int(point, base=base).to_bytes(32, "big", signed=False)

def str_to_byte(point: str, base: int) -> bytes:
    return int(point, base=base).to_bytes(4, "big", signed=False)


def bytes_to_u_array(val: bytearray, bitsize: int = 32, abi: bool = False) -> list:
    byte_jump = bitsize // 8
    array_arrays = [val[i : i + byte_jump] for i in range(0, len(val), byte_jump)]
    ubit_array = [str(int.from_bytes(x, "big", signed=False)) for x in array_arrays]
    if abi:
        ubit_array = ["0x" + str(int(x, 16)) for x in ubit_array]
    return ubit_array


def byte32_to_u32_array8(val: bytearray) -> list:
    if val == b"":
        fake_array = bytearray(32)
        return bytes_to_u_array(fake_array)

    assert len(val) == 32
    return bytes_to_u_array(val)


def decode_signature(signature: str) -> list:
    sig = decode_pubkey(signature)
    return bytes_to_u_array(sig, bitsize=64)


def decode_operation(operation: str) -> list:
    op = bytearray.fromhex(operation[2:])
    return ["0"] + bytes_to_u_array(op, bitsize=64)


def calculate_tree_root(values: List[bytearray]) -> bytearray:
    if len(values) == 1:
        return byte32_to_u32_array8(values[0])
    else:
        new_values = []
        for i in range(0, len(values), 2):
            if i == len(values) - 1:
                new_values.append(sha256(values[i], values[i]))
            else:
                new_values.append(sha256(values[i], values[i + 1]))
        return calculate_tree_root(new_values)

def concatenate_two_arrays_in_256(array1: List[str], array2: List[str]) -> List[bytearray]:
    result = []
    for i in range(0, len(array1)):
        result.append(sha256(str_to_byte(array1[i], 16), str_to_byte(array2[i], 16)))
    return result
