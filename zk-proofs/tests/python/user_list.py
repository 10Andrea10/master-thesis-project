import json
from utils import decode_pubkey, byte32_to_u32_array8

if __name__ == "__main__":
    num_users = 2048

    # Generate initial data
    pubkeys = [
        "edpku3EDFkXF2MHSipDKF2caz85yondEgqrohxdPdpXRpiX2tkFzuY",  # bob
        "edpkunwYWwaUUGPtbTGmggBB1dgmj5Ly8F9CwYHRL99XEDUgskgNBK",  # alice
        "edpkvRCLKPFrg7eYXLsKLjjZqYnsVtoZdRtF4RyzLzRFMHsqFrxpFF",  # john
        "edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH",  # jane
    ]
    
    for _ in range(num_users - 4 ):
        pubkeys.append("edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH")
    
    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]
    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]
    
    obj = json.dumps(
        [
            formatted_accounts,
        ],
        indent=4,
    )
    
    file_name = f"user-list-{num_users}.json"
    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)