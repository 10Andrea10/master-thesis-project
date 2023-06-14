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
        )

    @sp.entry_point
    def fooEntrypoint(self):
        pass

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
        pass




################################################################################################
#                                                                                              #
#                                                                                              #
#                                         REGISTRATION                                         #
#                                                                                              #
#                                                                                              #
################################################################################################
    
    # """
    # The entry point of the contract for a registration of a new user.

    # It receives a registration proof from the client and checks if it is valid.
    # - The 3 proofs are in params with the name received_proof_1, received_proof_2 and received_proof_3.
    # - The amount of accounts stored is in params with the name of NUMBER_OF_ACCOUNTS.
    # - The position of the new account is in params with the name of NEW_ACCOUNT_POSITION.
    # - The new account's public key is in params with the name of NEW_ACCOUNT_PUB_KEY.
    # """
    # @sp.entry_point
    # def receive_registration_proof(self, params):
    #     # Check if the current mr_pub_key is the same as the one received in the proof
    #     sp.for i in sp.range(0, 8):
    #         sp.verify(sp.to_int(self.data.mr_pub_key[i]) == sp.to_int(params.received_values[i]))
        
    #     # Check if the current mr_balance_nonce is the same as the one received in the proof
    #     sp.for i in sp.range(16, 24):
    #         sp.verify(sp.to_int(self.data.mr_balance_nonce.get(i-16)) == sp.to_int(params.received_values.get(i)))
        
    #     # TODO: put an if on the number of accounts passed as parameter and call the correct function
    #     self.register_new_with_4_accounts(params)
    
    # def register_new_with_4_accounts(self, params):
    #     self.verify_register_execution_4_accounts(params.received_values, params.received_proof_1, params.received_proof_2, params.received_proof_3)
    #     self.data.accounts[params.new_account_position].pub_key = params.new_account_pub_key
    #     self.data.accounts[params.new_account_position].mutez_balance = sp.utils.nat_to_mutez(0)
    #     self.data.accounts[params.new_account_position].nonce = 1
    
    # def verify_register_execution_4_accounts(self, input, proof_a, proof_b, proof_c):
    #     sp.set_type(input, sp.TBigMap(sp.TInt, sp.TBls12_381_fr)) 
        
    #     vk_h = sp.bls12_381_g2("0x0a1ff55d377bc5d9ad20881390e9149784a166f49bd77f46c3b58e5dd1baaed7bec0704943b3a8e6e34e8ec5fecbdde70338bfb672f3e2875b13f332965a771905dcf201fa8b80cefb0c15ef61bb3faf731f2338fa6e91af460c4596b286b93002b02204273442e2d593d40f3b389d9fc7343b31bd257e7337b0c3684f3b2c09613e3f07c295e3931a562283679a0b1910fdbdd62a38c8e25a3f089257d9ebdfe3b578bd8067d91f950ed310987dc68b1ec4aee0ed88f51bce064078a9ba201c")
    #     vk_g_alpha = sp.bls12_381_g1("0x15cfe029e52afb3f26099db6879c7a74e21bdf415fefda77b45e0cd82646cdc4aa4b1cd3e89aff5b0a62ad0da0d079ee01f4c444d2db5b4006e86f5c37595c24187c7b7e12a9c06664ce9912f46fbe13ed6993e0005f0856d11856617381bdc9")
    #     vk_h_beta = sp.bls12_381_g2("0x013c38300a0a0d9a40b574782dfae2269a1aec7375f00e4927fe9d6fe81634a6293868ece4fb9508688b9020dcec221206f8e408535846ae2535b3ac61bb90f365c4932542d3e74d6c8b48ba931530a003daaa48f12d3fea10d93fe2be2c2d44174407360dccd3c7a79c32dc757a457cb928dc1845298aa3e7fae79ee227b6074e3123a78b0902737021dc95bbcfc8c803ab0ceec72f8c0850a47d0c83b8669815ff8cac3c9e4af134307335a8baf465401e30dc5c8192785766ed305bcda68e")
    #     vk_g_gamma = sp.bls12_381_g1("0x07e1b28d85a85e7a9f5aa098db2b2952f6950fd663877309222c6bacbb3d5ee8a51ef52b3381dbaa81d626827d045d7619350a28fa3746f9affcb591eca01b1c371fc301d19f4af366811c196e0d19804201932668a324aba0b06a5daf658845")
    #     vk_h_gamma = sp.bls12_381_g2("0x0a1ff55d377bc5d9ad20881390e9149784a166f49bd77f46c3b58e5dd1baaed7bec0704943b3a8e6e34e8ec5fecbdde70338bfb672f3e2875b13f332965a771905dcf201fa8b80cefb0c15ef61bb3faf731f2338fa6e91af460c4596b286b93002b02204273442e2d593d40f3b389d9fc7343b31bd257e7337b0c3684f3b2c09613e3f07c295e3931a562283679a0b1910fdbdd62a38c8e25a3f089257d9ebdfe3b578bd8067d91f950ed310987dc68b1ec4aee0ed88f51bce064078a9ba201c")
    #     vk_query_not_local = {
	# 		0: sp.bls12_381_g1("0x04c9e62e122e241506c1b3082cff27209d27a4851a77b309f47d9e59f8675ec744ac5f06a8e9aa5ca9b0b557cb2d176401fcdec33baf541129996c83d05f8a3845c6ddbe9766349c831327b098800405c117cb043f847695ccdff27e40425d90"),
	# 		1: sp.bls12_381_g1("0x0c47d2816fb5c13fb1695aa67eab0bccc0e1ce17c4eb3f07aa906f831aa5fd0e9ad8b658b656809bb75b1dcf59d75fc001905bbdd821306b2b39edbc7d83a3cfb1c26a11b47ec45ab7319f86255157be0c52ce645be8b716c8e702f8105723ff"),
	# 		2: sp.bls12_381_g1("0x054c22d83b26c878c5b9b4a07dcc45b67255f1aa08bbcf8728446536205452cbf7157f28f14872a0ce863f0849a5a2130ff604ee64ecef7149da8cf6e7ae2e0b93b2349fc191476313127cfb1a3840782a59cfabc87ff1ad2700914e6a13ccc5"),
	# 		3: sp.bls12_381_g1("0x1323cfebaf362457ac2112824d9b02e19ab61b38f35f88ec8a7b26e0f7a5a5ab4ed536efa2d3f975fa2afe728911d48a036bd4769651ee67deb0c2f1302ac5f3547fbab76db35c8f946274a1f6e8af6d3f116b78c5eb544337cff28ff9ae1780"),
	# 		4: sp.bls12_381_g1("0x0e6632257764b73ea1f5c162b13db07a498c29cd57fa253236c8ef062934941747ee59a82002ec50965703558ac57ab10bd3f9c8f9612004e7d936e32fdf142d8e79849454ca5041fba261086372a81547f9011e723c6f1d4aed32c705f6958d"),
	# 		5: sp.bls12_381_g1("0x155a3db8d4e48e0cc0dc5dfd44ea7035bfb8baa32df0cf60fbc52de995d8513017d59bd637b49c888f846940b2c5bfa8080d2b85dae77cc1a4f7c3dc261e6bbc592ca9013477b4b9a76e72574c0308623ef77e193f593ad86c1a4f141007c934"),
	# 		6: sp.bls12_381_g1("0x06db304d091838f65fbbdedc39ba50f197e5dfbf4a9f0d9166e3bca3daf3046dc67e96118c038b4eb56ab3463e8e558a0ef35e556027ebeb66d5fb7d0e73545a65d58bcd6d5f8c140e13b582fc2aae541f344d42948db1d331e076f77fa96542"),
	# 		7: sp.bls12_381_g1("0x0bf0efe9bfa7bc3e7bae77bef318ae62547ad41f87d56b78b713fa5cdcd7670c4316e3aee73c224b21ba0d94315496700112ef5a673fa3e5041bd15bdaa18447fedb0b15a9561fdf0b1ff953f6766f1d4418febe41653db62bcd0f4d027e0368"),
	# 		8: sp.bls12_381_g1("0x0f11d03c2ce0738ab1e38883159f39cb7572dcce8ff2f697b6b427ce9d7c50411d60bfe2081e9d30ee2fce9ee6700c89137aa871b27fb533516481efd99fbd5a306b8be180c98fdf717d0cf8cf764690611b5cb7358c9764651f59ca26076260"),
	# 		9: sp.bls12_381_g1("0x0bf4936fe25f19ec0f25d5725309204a7d90df42ecf10156edf54831684d52cd48f7b163588990536f29f7ebe6e8e9e801d3d7eafad39b16ba64b0205d5f4ae2080d1bf6d500119dfb79e35bbe92a683e873c1f1811171f7e9149f67c8b97e27"),
	# 		10: sp.bls12_381_g1("0x1270ebb7b16ba92015128c52bf7c1f79876a7d53bbe9821195abe9ec888776a5e0332fe991b09464dcc4a58b9bb4c6c316b5a67f51d48be06dbdcf58edf548e7be4d0292f2dd6fc5ea7929adbe799e18ff57de390d8edf09d7c1accc2b3d916d"),
	# 		11: sp.bls12_381_g1("0x0afeb5f87a1bfc224956297941d70532bbf1aad3b7f82dbd350618405ffa63386db905769552e9d44f864b985b0df137106f7ebcbd1b92f1555cc2eeb61715fd8cab5473c542d7679f6787ce6fe7423c3eb5531907b3b3682f4acce71015ce45"),
	# 		12: sp.bls12_381_g1("0x0989d3814eb6fd5d352f7d3bb6fafca6e1a5afe32bc9a9fc1430315ee32aa83a68fcf8616986d23714b76c1b8c416b821518b9aac40afe4331f6fe771f1cc629e0d175df71358f16d65724d0b9b854a30e912206bcef26b2518784f7e9aa4068"),
	# 		13: sp.bls12_381_g1("0x11b72fafe4bd2d85e4f86fc94b7464ce9bfb90f14f7c2163d0071a1fe57bbbe16951abf8fb06ea0f6be320de01eb6435030c10fb2c324b058944c2d3cb043e494a91726cd46b822fb4f8ef02b2bf80320834e2c2440cf53396c8821cabcb61df"),
	# 		14: sp.bls12_381_g1("0x046b9ecbdaf585eee948b773dfffb91455f598b966b808ef402af225731b8280730cc0abc2458343c4cdf23830794b6308babdcc4a230dead7768b678d77f972e72f18a3b1adc9e7691a4529bdc7c5d55f771a270ac7ba95102421428022b8db"),
	# 		15: sp.bls12_381_g1("0x105822345e3abc92e2651782ed18f95499d53ee01c738bcfb19327d244064362e84aea862672ef75dec3bd0c131f0b840cc467306c1988442a1eee0b944e06e7dcf880f5ed2435005469723d243e9e51de78ee95bbbda24b72a7b8a6a987c3e5"),
	# 		16: sp.bls12_381_g1("0x19049fde06b3778fbde2daa16075edb819dfaa1baa18b4916fc6bc503b4d2d14560548dffc48d5a6581572b12601917e04c0292713c79e122a75b722d29ecca77ea57b4067d4c67df2bbb4a429deb1474823190c298cd1eef862c28550e9f380"),
	# 		17: sp.bls12_381_g1("0x1974132a0a3378ddf7a97576f5f71d9e31de99ca1690f6326c90730589db063c87fdeaf104bec66fd69a64dcbc47c39917839705f4bb037ab08f324c83aa491853b11e65fe99946a1be61a2e70d02cd2a4cc641ffbbcfd2c21ca6bdd6d5f2783"),
	# 		18: sp.bls12_381_g1("0x07a29e4550961c6e218454efabc55abdca2212df6d424fd828a5c155c7bc06714dda14b35806c749b00dd87d84e42a150757c34cce27d375dc23c4cf765c58eb18dfc0e0d256f4de0d1f3821a2c3727181e30cc9570f843c10a1869747517af8"),
	# 		19: sp.bls12_381_g1("0x165743e9eeebc7609a5f3f050188844bedfa96493fb054b912c0ef820ba189a57120e479b4a3b9b6bfedd47f92f017c602e8064116948d5148f6bef412338abbc0628ee39384c890cdd6f1554994d2f3cd7fd06e352e5c08add14bf4180c9b6f"),
	# 		20: sp.bls12_381_g1("0x0f993a5aae8d27266aef53b598fbbb82618665a4edb22188e6db2471d6d1bf65656860eee4796daab51dd9befee902860cc62b7caf552cf1213f5407f944fe378464b8bb4e021204813e37c67f434297f5f907b5258be54eada373e424ca5c6b"),
	# 		21: sp.bls12_381_g1("0x11fad8986bf2607563b760777114f2fbe1ee024ba997a6b76879f58813bcb1fe15320501f33451e5b7082a7e42a3d3be0b0be4de8701166b5a25f668f1ab3a988f7939e28096ff5a1f5da2d6e9a3ec83e35801e53bf640ca4d0999604f1b0352"),
	# 		22: sp.bls12_381_g1("0x15b236a832ab290c375cbe0cbc026cca3e3b033218af20ae6a8fde159e4b1ea17f1c59955fa84df2e31cba6683dd5bc519b0733cc139dee2515ccb6c6af691d3223ff8abb9c1af0d3e64e2975e54bb89ab80ab57fecb65736f40e1029d86951f"),
	# 		23: sp.bls12_381_g1("0x133db520071be6a0b0502a23665f2c2712aea253113e7e54f22b532dd5cb91e03502e1bc96b1808f512fbd16e02e4ce607359b99a978b1c9e8f42207e57f574e72eb6f63bcb350067061b8a6edf052a00c9d4f66b37dd409c02a5676a300d2e6"),
	# 		24: sp.bls12_381_g1("0x0b2f98ac98d5e40e5a3ffcbdb8d550ef71d166c49280bbfb3454f1e30ea57c430097e51b8c4affdad58148438488a51f178f2cf7e04ee7270330d5310959d292dab68b8dbf08bc47ec39a3e37169f6ba37b301359dcbf4d1677e5ba336145d32"),
	# 		25: sp.bls12_381_g1("0x1532347325e67d6ee5d32afa164ed28e36530642c2feb83e19e04194f531cfa1f0838233d88ede87f426c171440826a5035d1a5b7ffe4d6f8b412b3e6a1868e6e00948b5307a5d3e0347910ac076669eed92e122fa220b4ccfa46cc445c4f884"),
	# 		26: sp.bls12_381_g1("0x04fdda765f8186bf6400ca535b5dea3b58c709684fa844b0cdcb81d848f9a769fe6b14cc6ed73b087c43c12606ceb3c815bacea4ae083601b815b562b503eedf97a6ed9138945236ee4cec1685a0107aa4762dc8c3c1e37788b213c2e604d8b8"),
	# 		27: sp.bls12_381_g1("0x077933142b3fb03fdf3049925ae04067b58d2c0e7b751ec746421a598cbe0bc2c938ae17bf45a6db770a822d27d3a1730e01a47a7e58831ef5a1461775a089179e74557cba7e217f1bfb3f43c5e3dd6dc9e39e713e46d69c10bfa7059ebbe1c7"),
	# 		28: sp.bls12_381_g1("0x026bba8ad2552f5dfd122e6a48eaee1d2bac365ee737f98a488e69bb1df7ef9d272b636c67439f6c2eae6e26314869db191527b2887647126923ccc3a830800cc64c582e18d7da3b27f48af93d42f347368a93bbbb24426b5c64bb0e11c58adc"),
	# 		29: sp.bls12_381_g1("0x068afa8e51d9fa352817678b7b90363bca96ed9fd2dc7c3db17b03a754b85ac689e016adf675ae9c2a59f8531f5e5dc41128ac0d5056fc47d794993d2c60a5c931b0f6203c3dd77c563c53fbf30c92f11d5bfc1ddefe969e38205ff8f0e75237"),
	# 		30: sp.bls12_381_g1("0x09b56245cbb363f1e2329211065c6acd1a951dec63e2cc0451629e5cba19db1e9adbe0d61af4112402f3df464e3817a9002a5084601f329f81ee4a4b6c024a9e14a9aa1f148cd0517c8b7b8cd3c79b1a7eba61708989dc5d513e956f519333dd"),
	# 		31: sp.bls12_381_g1("0x0ee68d158bfa0b5dd0025d6d8fd380f8f7f06482a84f033ab05cd776ce9aa71065bcb0e17303030acd2cedf13ef247f218aabaa513c01f3ddb48ef7ef6d193607d432fd5362412486165f490d7b8cff213708b1686ce921c0bdd360def784156"),
	# 		32: sp.bls12_381_g1("0x0e77a906210ba4a29f883e82a54734fb19877f0f3893ac18e8de3c3cbea944d518045e6691e1a71f8e4e0227270da7c815db4d583c23e7afd8f341c9336bcb1be9997da4c22da8792a34802259e856ffec56aec66aeef223d73ba897beaa3e74"),
	# 		33: sp.bls12_381_g1("0x10cbe40d0a4e26c1e213cb3e95abd82f3c75fd5991370ba41e791f876faa2aef935a4913297793823b31b563063aa38b0776a08c25de196fa4841c159414ceb8522c0c3e677ada31f8e5c2ee780b79ab9c622f2294847c55c106fd80c47cf52e"),
	# 		34: sp.bls12_381_g1("0x16bc27108a00566a750f574052b308a00f53b43a97f85a997ebe2804b177cd6fc0ad8fc8250b4bf4b383de14867c6f8a0b6b2e487e93dbc69d4688be754b86b03db0c57d890709a717cbae7a0977620d687b0e45c066de2b333bf5c12aa666b1"),
	# 		35: sp.bls12_381_g1("0x19605fefeb9b04dd191af393a595e6c15717e1bd03fee0fe2984f60f89e5f5d1a136bd3020d4157c48d25cce81f2e0a10051599d27b09d96bca99a29797b98b2f278c4226f6c02ede43e45840e306e6de4ef1d4b5563d847e5650def94977f1b"),
	# 		36: sp.bls12_381_g1("0x19bdc8f28d8aeda65d010712167392ac9a7e1ba4cb5de2edcf0a6915a7a92ce70bb724cf4c802eb053dfb3a9d34deae60a5ed735664f64cec8f640bf42bcce8570c6d872161fa5e90ed141fe6e91e686a619e1d2dcd3389994304eba85c203c6"),
	# 		37: sp.bls12_381_g1("0x0d8f3dbeafe72ea445ff9dd2a200135cb457263a29159e499729e928411aa1153f7ac019df62d4ab9f932b6e3436724710d615b84c06e05aa053a6119267c3d7af24c939411ab00728ea410f77d52add8bf23bebb1a85d0ebb3432f161e58d88"),
	# 		38: sp.bls12_381_g1("0x136eee152f8bf491e9586a86738ce644ef7b65ad1c48f3c3587adbd8a4f7ca790f1a3c94aac48d6fcb8163b3db85bbdf0a1e4b0e7d1852e2e6322ee1179896f8bf6d73e1cb8a2351b861f7b614082442a911dac2e5cd79738c29bbb85f3d3da8"),
	# 		39: sp.bls12_381_g1("0x024ecad0e89195c1d9e98768d423bcb57c878fad97ebef096e3aae0d1bd7559b7018a3db52aef2e223405a1b50602639190e04575653b948fd28eb39b739a35f2b9242b1ebe1c881a917fc175ca1ba1a5e4e094deda0a846a91f4b3ba5a2ece7"),
	# 		40: sp.bls12_381_g1("0x01c549b263415a2dbae72a1492e252d857279ca35fb65cb36454da9f6b4a44e4fb10d22c9090e5251de4cdf24160c324041f33d15d2da4d55b5db115b305451e13f188c7beb89f43cce07d893954a6f77365afaa87f24916d0978cf20b7be062")
	# 	}
        
    #     vk_query = sp.local('vk_query', vk_query_not_local)

    #     vk_x_not_local  = sp.mul(vk_query.value[1], input[0]) 
    #     vk_x = sp.local('vk_x', vk_x_not_local)
        
    #     # sp.range(x, y) goes from x (inclusive) to y (exclusive)
    #     sp.for i in sp.range(1, sp.len(vk_query.value)-1):
    #         vk_x.value = vk_x.value + sp.mul(vk_query.value[i+1], input[i])

    #     vk_x.value = vk_x.value + vk_query.value[0]     

    #     list_pair1 = sp.list([
    #         sp.pair(vk_g_alpha,vk_h_beta),
    #         sp.pair(vk_x.value,vk_h_gamma),
    #         sp.pair(proof_c,vk_h),
    #         sp.pair(- (proof_a+vk_g_alpha),proof_b+vk_h_beta)
    #     ])

    #     list_pair2 = sp.list([
    #         sp.pair(proof_a,vk_h_gamma),
    #         sp.pair(- vk_g_gamma,proof_b)
    #     ])

    #     check1 = sp.pairing_check(list_pair1)
    #     check2 = sp.pairing_check(list_pair2)
    #     sp.if check1 != True:
    #         sp.failwith("The proof is not valid, check1 failed")
    #     sp.if check2 != True:
    #         sp.failwith("The proof is not valid, check2 failed")


sp.add_compilation_target("Rollup", ZKRollupContract())