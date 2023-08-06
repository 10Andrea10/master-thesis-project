import smartpy as sp

INITIAL_SIZE = 4
class ZKRollupContract(sp.Contract):
    def __init__(self, map):
        self.init(
            last_rollup_timestamp = sp.timestamp_from_utc_now(),
            accounts =  map,
            mr_pub_key = {
                0: sp.bls12_381_fr("0x61e6b163ed46ca6bb227bf778950d31d22569904d7898331035124f553c5111e"),
                1: sp.bls12_381_fr("0x8ECE7B9200000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0x2890006E00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0x200A3A8300000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0x0CE12D8600000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0xC49E221D00000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0xDBB1ACD100000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0x2949C0A100000000000000000000000000000000000000000000000000000000"),
            },
            mr_balance_nonce = {
                0: sp.bls12_381_fr("0x0A78205E00000000000000000000000000000000000000000000000000000000"),
                1: sp.bls12_381_fr("0x2E1717F400000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0xCD5E373B00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0x81E26C7600000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0x3F5226A800000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0x7013C8F400000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0xAB6C0A6700000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0xB04AAC3B00000000000000000000000000000000000000000000000000000000"),
            },
            deposit_queue = sp.map(
                l = {},
                tkey = sp.TNat,
                tvalue = sp.TMutez
            ),
            current_size = sp.nat(INITIAL_SIZE),
        )
    
    def initial_checks_mr(self, params):
        sp.set_type(params.received_values, sp.TBigMap(sp.TInt, sp.TBls12_381_fr))

        # Check if the current mr_pub_key is the same as the one received in the proof
        sp.for i in sp.range(0, 8):
            sp.verify(sp.to_int(self.data.mr_pub_key[i]) == sp.to_int(params.received_values[i]))
        
        # Check if the current mr_balance_nonce is the same as the one received in the proof
        sp.for i in sp.range(8, 16):
            sp.verify(sp.to_int(self.data.mr_balance_nonce.get(i - 8)) == sp.to_int(params.received_values.get(i)))
    
    def send_verification(self, params, contract_address, entrypoint):
        contractParams = sp.contract(
        sp.TRecord(
                input = sp.TBigMap(sp.TInt, sp.TBls12_381_fr),
                proof_a = sp.TBls12_381_g1,
                proof_b = sp.TBls12_381_g2,
                proof_c = sp.TBls12_381_g1
            ),
            sp.address(contract_address),
            entry_point = entrypoint
        ).open_some()

        dataToBeSent = sp.record(input = params.received_values, proof_a = params.received_proof_1, proof_b = params.received_proof_2, proof_c = params.received_proof_3)
        sp.transfer(dataToBeSent,sp.mutez(0),contractParams)

    def set_mr_data(self, params, pos_first_element_new_root_balances_nonces, pos_first_element_new_root_public_keys):
        sp.for i in sp.range(0, 8):
            self.data.mr_balance_nonce[i] = params.received_values[i + pos_first_element_new_root_balances_nonces.value ]
        sp.for i in sp.range(0, 8):
            self.data.mr_pub_key[i] = params.received_values[i + pos_first_element_new_root_public_keys.value ]


################################################################################################
#                                                                                              #
#                                                                                              #
#                                            ROLLUP                                            #
#                                                                                              #
#                                                                                              #
################################################################################################

    @sp.entry_point
    def receive_rollup_proof(self, params):
        self.initial_checks_mr(params)
        sp.set_type(params.transaction_number, sp.TNat)

        sp.if params.transaction_number == 30:
            self.rollup_4_30(params)
        sp.if params.transaction_number == 50:
            self.rollup_4_50(params)

                
    def rollup_4_30(self, params):
        entry_point = "verify_rollup_4_30"
        verification_contract = "KT1CJv9KR13Mqj3XihgpKUi6wRcte5HW1QtZ"
        self.rollup_generic(params, entry_point, verification_contract, 136, 144, 148)
    
    def rollup_4_50(self, params):
        entry_point = "verify_rollup_4_50"
        verification_contract = "KT1UNt2YPSMLRmSfE9aVWFygfKU4uPwkU7aV"
        self.rollup_generic(params, entry_point, verification_contract, 216, 224, 228)
    
    def rollup_generic(self, params, entry_point, verification_contract, first_el_new_r_b_n, firs_bal, first_nonce):
        self.send_verification(params, verification_contract, entry_point)
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(first_el_new_r_b_n))
        pos_first_balance_in_received_values = sp.local('pos_first_balance_in_received_values', sp.int(firs_bal))
        pos_first_nonce_in_received_values = sp.local('pos_first_nonce_in_received_values', sp.int(first_nonce))
        sp.for i in sp.range(0, self.data.current_size):
            # Conversions explanation:
            # - sp.utils.nat_to_mutez(sp.as_nat(sp.to_int( is because we're receiving types of sp.TBls12_381_fr and we need to convert them to mutez
            # - sp.to_int(i) is because the sp.range wanted a nat but to access a map we need an int, idk why since it's a big map declared with tkey = sp.TNat
            self.data.accounts[i].mutez_balance = sp.utils.nat_to_mutez(sp.as_nat(sp.to_int(params.received_values[ sp.to_int(i) + pos_first_balance_in_received_values.value])))
            self.data.accounts[i].nonce = sp.as_nat(sp.to_int(params.received_values[ sp.to_int(i) + pos_first_nonce_in_received_values.value]))
            self.data.last_rollup_timestamp = sp.timestamp_from_utc_now()
        sp.for i in sp.range(0, 8):
            self.data.mr_balance_nonce[i] = params.received_values[i + pos_first_element_new_root_balances_nonces.value ]

        
    
################################################################################################
#                                                                                              #
#                                                                                              #
#                                          DEREGISTER                                          #
#                                                                                              #
#                                                                                              #
################################################################################################

    @sp.entry_point
    def receive_deregister_proof(self, params):
        self.initial_checks_mr(params)

        # TODO: put an if based on the number of accounts
        self.deregister_with_4_accounts(params)
    

    def deregister_with_4_accounts(self, params):
        entry_point = "verify_deregister_4"
        verification_contract = "KT1HztMKaPu7LET3Qj5P1gGMurv3tPArFdjD"

        self.send_verification(params, verification_contract, entry_point)
        # TODO: edit indexes if proof changes
        pos_first_element_new_root_public_keys = sp.local('pos_first_element_new_root_public_keys', sp.int(17))
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(25))
        pos_position_value = sp.local('pos_position_value', sp.int(16))

        # TODO: check this function is working
        self.set_mr_data(params, pos_first_element_new_root_balances_nonces, pos_first_element_new_root_public_keys)

        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].mutez_balance = sp.mutez(0)
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].nonce = sp.nat(0)
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].pub_key = sp.none



################################################################################################
#                                                                                              #
#                                                                                              #
#                                           REGISTER                                           #
#                                                                                              #
#                                                                                              #
################################################################################################


    @sp.entry_point
    def receive_register_proof(self, params):
        self.initial_checks_mr(params)

        # TODO: put an if based on the number of accounts
        self.register_with_4_accounts(params)
    

    def register_with_4_accounts(self, params):
        entry_point = "verify_register_4"
        verification_contract = "KT1PTq7B96pHeviRaJZ4hq84fZYPcWfQ4Rcp"

        self.send_verification(params, verification_contract, entry_point)
        # TODO: edit indexes if proof changes
        pos_first_element_new_root_public_keys = sp.local('pos_first_element_new_root_public_keys', sp.int(25))
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(33))
        pos_position_value = sp.local('pos_position_value', sp.int(16))

        self.set_mr_data(params, pos_first_element_new_root_balances_nonces, pos_first_element_new_root_public_keys)
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].mutez_balance = sp.mutez(0)
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].nonce = sp.nat(1)

        # TODO: convert the pubkey array from the received_values to a sp.key. I don't knwo how to do it
        # so I pass directly the pubkey of the new user. May be a security risk because the pubkey may be modified
        # by the server sending the proof.
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].pub_key = params.new_user_pub_key

################################################################################################
#                                                                                              #
#                                                                                              #
#                                           DEPOSIT                                            #
#                                                                                              #
#                                                                                              #
################################################################################################

    @sp.entry_point
    def deposit(self, params):
        sp.set_type(params.account_index, sp.TNat)
        sp.set_type(params.account_public_key, sp.TKey)
        # Check sender is the user
        sp.to_address(sp.implicit_account(sp.hash_key(params.account_public_key)))
        converted_address = sp.to_address(sp.implicit_account(sp.hash_key(params.account_public_key)))
        sp.if sp.sender != converted_address:
            sp.failwith("Sender is different from the sent public key")
        sp.verify(params.account_public_key == self.data.accounts[params.account_index].pub_key.open_some(message = "No user registered in this position") , message = "Not authorized to deposit")
        self.data.deposit_queue[params.account_index] = self.data.deposit_queue.get(
                params.account_index,
                default_value = sp.mutez(0)
            ) + sp.amount
    
    @sp.entry_point
    def receive_deposit_proof(self, params):
        self.initial_checks_mr(params)

        # TODO: put an if based on the number of accounts
        self.deposit_with_4_accounts(params)
    
    def deposit_with_4_accounts(self, params):
        entry_point = "verify_deposit_4"
        verification_contract = "KT1XbemZ7U57363QdE8YCc7ozb6UHqwi7YmX"

        self.send_verification(params, verification_contract, entry_point)
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(16))
        sp.for i in sp.range(0, 8):
            self.data.mr_balance_nonce[i] = params.received_values[i + pos_first_element_new_root_balances_nonces.value ]
        sp.for i in self.data.deposit_queue.keys():
            self.data.accounts[i].mutez_balance += self.data.deposit_queue.get(i)
            del self.data.deposit_queue[i]
        
################################################################################################
#                                                                                              #
#                                                                                              #
#                                           WITHDRAW                                           #
#                                                                                              #
#                                                                                              #
################################################################################################


    @sp.entry_point
    def receive_withdraw_proof(self, params):
        self.initial_checks_mr(params)

        # TODO: put an if based on the number of accounts
        self.withdraw_with_4_accounts(params)
    
    def withdraw_with_4_accounts(self, params):
        entry_point = "verify_withdraw_4"
        verification_contract = "KT1RNqm9DDSYDBj1XBHj4qz1TpgnMmomuTgq"

        self.send_verification(params, verification_contract, entry_point)
        # TODO: edit indexes if proof changes
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(18))
        pos_position = sp.local('pos_position', sp.int(16))
        pos_amount = sp.local('pos_amount', sp.int(17))

        sp.for i in sp.range(0, 8):
            self.data.mr_balance_nonce[i] = params.received_values[i + pos_first_element_new_root_balances_nonces.value ]
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position.value]))].mutez_balance -= sp.utils.nat_to_mutez(sp.as_nat(sp.to_int(params.received_values[pos_amount.value])))

        # send the amount to the user
        destination_address = sp.to_address(sp.implicit_account(sp.hash_key(self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position.value]))].pub_key.open_some())))
        amount = sp.utils.nat_to_mutez(sp.as_nat(sp.to_int(params.received_values[pos_amount.value])))
        sp.send(destination_address, amount)

################################################################################################
#                                                                                              #
#                                                                                              #
#                                            RESIZE                                            #
#                                                                                              #
#                                                                                              #
################################################################################################

    @sp.entry_point
    def resize_DEV(self, params):
        sp.set_type(params.size, sp.TNat)
        sp.for i in sp.range (self.data.current_size, params.size):
            self.data.accounts[i] = sp.record(
                    pub_key = sp.none,
                    mutez_balance = sp.mutez(0),
                    nonce = sp.nat(0),
                    )
        self.data.current_size = params.size


def initialise_map():
    map = {
        0: sp.record(
                    pub_key = sp.some(sp.key("edpku3EDFkXF2MHSipDKF2caz85yondEgqrohxdPdpXRpiX2tkFzuY")),
                    mutez_balance = sp.mutez(50331648),
                    nonce = sp.nat(1),
        ),
        1: sp.record(
                    pub_key = sp.some(sp.key("edpkunwYWwaUUGPtbTGmggBB1dgmj5Ly8F9CwYHRL99XEDUgskgNBK")),
                    mutez_balance = sp.mutez(83886080),
                    nonce = sp.nat(1),
        ),
        2: sp.record(
                    pub_key = sp.some(sp.key("edpkvRCLKPFrg7eYXLsKLjjZqYnsVtoZdRtF4RyzLzRFMHsqFrxpFF")),
                    mutez_balance = sp.mutez(0),
                    nonce = sp.nat(1),
        ),
        3: sp.record(
                    pub_key = sp.some(sp.key("edpktz9mUY7GeEbieZTsL2RwmA2GhwBd9YsYvRbnSFWnbb6pZX9aYH")),
                    mutez_balance = sp.mutez(0),
                    nonce = sp.nat(1),
        ),
    }
    return sp.big_map(
    l = map,
    tkey = sp.TNat,
    tvalue = sp.TRecord(
        pub_key = sp.TOption(sp.TKey),
        mutez_balance = sp.TMutez,
        nonce = sp.TNat,
    )
)

sp.add_compilation_target("Rollup", ZKRollupContract(initialise_map()))