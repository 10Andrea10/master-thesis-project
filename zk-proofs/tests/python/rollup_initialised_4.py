import json
from utils import decode_pubkey, calculate_tree_root, concatenate_two_arrays_in_256, byte32_to_u32_array8
from utils_zok import calculate_tree_root_zok

if __name__ == "__main__":
    num_users = 4
    num_transactions = 3

    # Generate initial data
    pubkeys = [
        "edpku3EDFkXF2MHSipDKF2caz85yondEgqrohxdPdpXRpiX2tkFzuY",  # bob
        "edpkunwYWwaUUGPtbTGmggBB1dgmj5Ly8F9CwYHRL99XEDUgskgNBK",  # alice
        "edpkvRCLKPFrg7eYXLsKLjjZqYnsVtoZdRtF4RyzLzRFMHsqFrxpFF",  # john
        "edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH"  # jane
    ]

    signatures = [
        {
            "r": [
                "5164499298436505371072105668521112783967459446400705593773774843659785323798",
                "49465128908838764969820259532503381450210077275440112030771876533218138154985"
            ],
            "s": "4783138945796921273862212240934263048982849875421100388381447563093604986101",
            "a": [
                "9463778183056102078866993118044984671658132484107251542179921426381620273800",
                "4635611125295530335317425380928224173124053237108412540578596412445271041431"
            ]
        },
        {
            "r": [
                "20036951508540731851894555453806128871680283739948515047236830912069055648233",
                "51522621372507515319465794092941408366652862766421027293018066523807120050424"
            ],
            "s": "5475947179309841157262453697393341138816089901286499716012733689247046164849",
            "a": [
                "9463778183056102078866993118044984671658132484107251542179921426381620273800",
                "4635611125295530335317425380928224173124053237108412540578596412445271041431"
            ]
        },
        {
            "r": [
                "18222851952372333926274480140504867052789981596947869650909032302983719415779",
                "18061585656819318692328562819598212585316716773475121384991718500753028132978"
            ],
            "s": "2339252480543022442078362723527353874993926337389378893921912730045162396271",
            "a": [
                "9463778183056102078866993118044984671658132484107251542179921426381620273800",
                "4635611125295530335317425380928224173124053237108412540578596412445271041431"
            ]
        }
    ]

    decoded_pubkeys = [decode_pubkey(x) for x in pubkeys]
    formatted_accounts = [byte32_to_u32_array8(x) for x in decoded_pubkeys]
    # account_root = calculate_tree_root(decoded_pubkeys)
    # account_root_poseidon = calculate_tree_root_zok(decoded_pubkeys)

    account_root = "0x61e6b163ed46ca6bb227bf778950d31d22569904d7898331035124f553c5111e"
    concatenatedBalancesNoncesTreeRoot = "0x3b6e8e4938036678662056092f901cf833af129c5f04ca1f2319bc66e0804c27"

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

    file_name = f"rollup-initialised-{num_users}-{num_transactions}-inputs.json"

    with open(f"output_files/{file_name}", "w") as outfile:
        outfile.write(obj)
