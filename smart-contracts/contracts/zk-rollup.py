import smartpy as sp
class ZKRollupContract(sp.Contract):
    def __init__(self):
        self.init(
            last_rollup_timestamp = sp.timestamp_from_utc_now(),
            accounts =  sp.big_map(
                l = {
                    0 : sp.record(
                        pub_key = sp.key("edpkurPsQ8eUApnLUJ9ZPDvu98E8VNj4KtJa1aZr16Cr5ow5VHKnz4"),
                        mutez_balance = sp.mutez(3000000),
                        nonce = sp.nat(1),
                    ), 
                    1 : sp.record(
                        pub_key = sp.key("edpkvGfYw3LyB1UcCahKQk4rF2tvbMUk8GFiTuMjL75uGXrpvKXhjn"),
                        mutez_balance = sp.mutez(5000000),
                        nonce = sp.nat(1),
                    ),
                    2 : sp.record(
                        pub_key = sp.key("edpktt6t2ENhxiQqun6bXPPWC6tFVvNPTDRh1gEPGX4BgDgbDnmGzP"),
                        mutez_balance = sp.mutez(0),
                        nonce = sp.nat(1),
                    ), 
                    3 : sp.record(
                        pub_key = sp.key("edpkvS6TDSWcqqj3EJi3NRrCMyN7oNw1B3Hp37R19tMThqM8YNhAuS"),
                        mutez_balance = sp.mutez(0),
                        nonce = sp.nat(1),
                    ), 
                },
                tkey = sp.TNat,
                tvalue = sp.TRecord(
                    pub_key = sp.TKey,
                    mutez_balance = sp.TMutez,
                    nonce = sp.TNat,
                )
            ),
            mr_pub_key = {
                0: sp.bls12_381_fr("0xC145EF0800000000000000000000000000000000000000000000000000000000"),
                1: sp.bls12_381_fr("0x2ACC5FF700000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0x1278102D00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0x7A0239BB00000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0x004A2D3F00000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0x050D53FF00000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0x0473569500000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0x4D05A21800000000000000000000000000000000000000000000000000000000"),
                },
            mr_balance_nonce = {
                0: sp.bls12_381_fr("0x0DABDF9300000000000000000000000000000000000000000000000000000000"),
                1: sp.bls12_381_fr("0xCD52D5BF00000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0xC23FD67E00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0x9E0A6FB600000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0xCAD935A500000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0x5E3ADADD00000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0xC7F3A80F00000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0x5B9AE47900000000000000000000000000000000000000000000000000000000"),
            },
            money_queue = sp.map(
                l = {},
                tkey = sp.TNat,
                tvalue = sp.TInt
            ),
        )

    def initial_checks_mr(self, params):
        # TODO: check if typing is correct
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

        # TODO: put an if on the number of accounts passed as parameter and call the correct function
        self.rollup_with_4_accounts(params)

                
    def rollup_with_4_accounts(self, params):
        entry_point = "verify_rollup_4"
        verification_contract = "KT1NDPhNvUhPCbYiGfqV8fqdCib1PQef7C8y"

        self.send_verification(params, verification_contract, entry_point)

        # TODO: change if the proof index changes
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(28))
        pos_first_balance_in_received_values = sp.local('pos_first_balance_in_received_values', sp.int(36))
        pos_first_nonce_in_received_values = sp.local('pos_first_nonce_in_received_values', sp.int(40))
        sp.for i in sp.range(0, sp.as_nat(4)):
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
        verification_contract = "KT1GHx1UEG3X14w4yybnNhux7HcmKkj42F8V"

        self.send_verification(params, verification_contract, entry_point)
        # TODO: edit indexes if proof changes
        pos_first_element_new_root_public_keys = sp.local('pos_first_element_new_root_public_keys', sp.int(17))
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(25))
        pos_position_value = sp.local('pos_position_value', sp.int(16))

        # TODO: check this function is working
        self.set_mr_data(params, pos_first_element_new_root_balances_nonces, pos_first_element_new_root_public_keys)

        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].mutez_balance = sp.mutez(0)
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].nonce = sp.nat(0)
        # This is a valid pulic key, and it's the one used for the tests. It's because it is not possible to 
        # have a public key with all 0s.
        self.data.accounts[sp.as_nat(sp.to_int(params.received_values[pos_position_value.value]))].pub_key = sp.key("edpkuY4Le5Ps78zDSaHqJDuEa7HCbNEu6x5aD3fwiEHL3LR87bGer4")



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
        verification_contract = "KT1DJHmfU1nRTweMraKsvgzxb7ZxRLZKa5KP"

        self.send_verification(params, verification_contract, entry_point)
        # TODO: edit indexes if proof changes
        pos_first_element_new_root_public_keys = sp.local('pos_first_element_new_root_public_keys', sp.int(25))
        pos_first_element_new_root_balances_nonces = sp.local('pos_first_element_new_root_balances_nonces', sp.int(33))
        pos_position_value = sp.local('pos_position_value', sp.int(16))
        # pos_first_element_new_account_pubkey = sp.local('pos_first_element_new_account_pubkey', sp.int(17))

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
        sp.verify(params.account_public_key == self.data.accounts[params.account_index].pub_key, message = "Not authorized to deposit")
        self.data.money_queue[params.account_index] = self.data.money_queue.get(
                params.account_index,
                default_value = sp.int(0)
            ) + sp.to_int(sp.utils.mutez_to_nat(sp.amount))
        


sp.add_compilation_target("Rollup", ZKRollupContract())