from utils import sha256

if __name__ == "__main__":
    a = bytearray.fromhex("6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19")
    b = bytearray.fromhex("7a3f97c7 c8c0c04a 118d1b25 68ec9f7c 34ee7c8d 1c1af1d8 f6a29e91 cdbbc177")

    res = sha256(a, b).hex()
    print(res)
