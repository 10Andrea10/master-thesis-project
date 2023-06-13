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

    """
    The entry point of the contract for a rollup execution.

    It receives a rollup proof from the client and checks if it is valid.
    - The output values are in params with the name received_values.
    - The 3 proofs are in params with the name received_proof_1, received_proof_2 and received_proof_3.
    - The amount of accounts stored is in params with the name of NUMBER_OF_ACCOUNTS. It is necessary
        as the contract cannot iterate over a Big Map but an external service using an rpc can. And
        it will be used in future to support a variable number of accounts.
    """
    @sp.entry_point
    def receive_rollup_proof(self, params):

        # Check if the current mr_pub_key is the same as the one received in the proof
        sp.for i in sp.range(0, 8):
            sp.verify(sp.to_int(self.data.mr_pub_key[i]) == sp.to_int(params.received_values[i]))
        
        # Check if the current mr_balance_nonce is the same as the one received in the proof
        sp.for i in sp.range(8, 16):
            sp.verify(sp.to_int(self.data.mr_balance_nonce.get(i - 8)) == sp.to_int(params.received_values.get(i)))

        # TODO: put an if on the number of accounts passed as parameter and call the correct function
        self.rollup_with_4_accounts(params)

    """
    The entry point of the contract for a registration of a new user.

    It receives a registration proof from the client and checks if it is valid.
    - The 3 proofs are in params with the name received_proof_1, received_proof_2 and received_proof_3.
    - The amount of accounts stored is in params with the name of NUMBER_OF_ACCOUNTS.
    - The position of the new account is in params with the name of NEW_ACCOUNT_POSITION.
    - The new account's public key is in params with the name of NEW_ACCOUNT_PUB_KEY.
    """
    @sp.entry_point
    def receive_registration_proof(self, params):
        # Check if the current mr_pub_key is the same as the one received in the proof
        sp.for i in sp.range(0, 8):
            sp.verify(sp.to_int(self.data.mr_pub_key[i]) == sp.to_int(params.received_values[i]))
        
        # Check if the current mr_balance_nonce is the same as the one received in the proof
        sp.for i in sp.range(16, 24):
            sp.verify(sp.to_int(self.data.mr_balance_nonce.get(i-16)) == sp.to_int(params.received_values.get(i)))
        
        # TODO: put an if on the number of accounts passed as parameter and call the correct function
        self.register_new_with_4_accounts(params)



                
    def rollup_with_4_accounts(self, params):
        # The verify function is called.
        self.verify_rollup_execution_4_accounts(params.received_values, params.received_proof_1, params.received_proof_2, params.received_proof_3)

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
    

    def register_new_with_4_accounts(self, params):
        self.verify_register_execution_4_accounts(params.received_values, params.received_proof_1, params.received_proof_2, params.received_proof_3)
        self.data.accounts[params.new_account_position].pub_key = params.new_account_pub_key
        self.data.accounts[params.new_account_position].mutez_balance = sp.utils.nat_to_mutez(0)
        self.data.accounts[params.new_account_position].nonce = 1

    """
    The verification function that checks if the proof is valid.

    It stores in the last_rollup_verified the outcome of the verification and updates accordingly last_rollup_timestamp
    """
    def verify_rollup_execution_4_accounts(self, input, proof_a, proof_b, proof_c):
        sp.set_type(input, sp.TBigMap(sp.TInt, sp.TBls12_381_fr)) 
        
        vk_h = sp.bls12_381_g2("0x093f5ea81b6b5b16fdfa9879c8e41b345978d5da9157239af5ae004eaf7b1880661981dc44136b3c0d79a600a4f9ef400113cfafcfc63a559db34e2dd9aa58fe3f608841400b9b768c777293fd5d6815f26d1c1edce7213f486a53642399702d0b8b382c51d72ba00419d9a61d93fc31c500df8b261d12001b52079071201e317e11b71403ad49aacc2bf99c9ad2538c0faa6470febb98de5811a74e8e9b4083480316932681e69a2e5eb2597a5227ce243c8729b43fd2e0eb4488db18922bae")
        vk_g_alpha = sp.bls12_381_g1("0x02804d44b928719a196d2480ba900334f5ff740ae83987c0b0c98bea8cbf8ea4a86e6749b9a714a11c963e6ec03bf384001853c18ef97ffe6e2ce2cf728e5854b970cbc42be9b190a5f3ac49ec116bcf7e79db30e3de6cbeb9d3d6979c42a284")
        vk_h_beta = sp.bls12_381_g2("0x19111d1f124fdcebab9b69bc8831ba359efd572b697493f33ee4ce624d08523eae538a657537913f91fb91865f67277f13fb726af8b6f231ec6d23eee81657dd6788837bf373d150b6709aa6191549a3d0101f1b7b739b1e8d7b8ce1aeaf9c3008d6716c58b41a75d7f225355bbb5034d5289a9fee46bc0adf674a51b63caf01f43c377679dec4e7d9866eeeaae9b90f001bf549a0ab199fcea883aed86c796d96d1cb8344bc3cde0279475a2edf247ebad372847a181b6e11374c3478292bb0")
        vk_g_gamma = sp.bls12_381_g1("0x1482c5a0eba460dce7ef7d31f8969efc5a96ac23f2a467a5fa68f840782a010f4d80ca779fa3059e149e9480ac391c55195fc6e3dd753d619f6e027d7fdda92d1299b84095ee666de0f2b4fc685e0ea3c536c29f0c1b21959f3f78e48f0e3e92")
        vk_h_gamma = sp.bls12_381_g2("0x093f5ea81b6b5b16fdfa9879c8e41b345978d5da9157239af5ae004eaf7b1880661981dc44136b3c0d79a600a4f9ef400113cfafcfc63a559db34e2dd9aa58fe3f608841400b9b768c777293fd5d6815f26d1c1edce7213f486a53642399702d0b8b382c51d72ba00419d9a61d93fc31c500df8b261d12001b52079071201e317e11b71403ad49aacc2bf99c9ad2538c0faa6470febb98de5811a74e8e9b4083480316932681e69a2e5eb2597a5227ce243c8729b43fd2e0eb4488db18922bae")
        vk_query_not_local = {
			0: sp.bls12_381_g1("0x01b0b40e5f208c19b8879e8196b4a4bee6b8b46a64905c0523d00bee8e059af445dd8dd504e2f50bd2302c0fad76792312c934c49931b682d2aca902a6a4ec7ee339ce0732ccd9f29b9134f50b2b5e73886301493c643450bd8efbe83f0fc18b"),
			1: sp.bls12_381_g1("0x0dd69040cac2d10990817ae8353513034df401243f9d79d8d95b9c9fe256840aa9feefa657a20ad6447cb7d10d2b46ee18acdacd69c9148c371e01a05fed21c3a2db57fe9dfc24ca98e6b3fdee15a69a6afd6a6d13ce72d0e6250fbe588243e2"),
			2: sp.bls12_381_g1("0x13c912f9090499443d4bc4acd72e3fd6962403c204c338bdd2d785576079ae6fe677d26ae56a6c3141b70f8942c1b179039ab2ca5e0118e7ff67c1dbca362aaf7d00f6b030cb451a5d30ac2c8be9c6a26695037c00ab20b5cb8eed1e932be906"),
			3: sp.bls12_381_g1("0x02849ef7ba6fe12e651d67ce044dd83c676e396da7260b09fd1c53043c912a51ea0b1e74e98b8d4bf4708891f7d0c549178d947d5caf9278e6ed51e98194b3d0ff0ed8e298c15bc8715a6560769fc29b10e15ac570edcb06590c05bc03895f79"),
			4: sp.bls12_381_g1("0x039de3d18c82e2526793b862319e953192818ad454f5d36b4deed540957f71e96233dd9d8a64710f60c8c7c37a055c8102aaa4c0a204cae0627f13876a3277836cb15e495cf4421b0209c884e33c6efd2e19e9309b3ab83947ff7a2722589e3a"),
			5: sp.bls12_381_g1("0x03cafe6b4ff168e8ae65802983d42a129fa76e38090a4980879dd42f822a3eb54d24793887e6862d65136a18abeb8d431015a10631e1c89907e26c59807681a21209f48217c1314863c77a1663ce10f52312f51a716a20722d92502b62ee556f"),
			6: sp.bls12_381_g1("0x1499c363d475e3dc4de23fbb416bc8dbe381694a599d94369bdd8803c58c3c9469d9b3018a2e0cf6471954ebc9f847bc123eac14ac126a3448502f8cb3d839a445e51bed6b54d5034671d81adf80db7bc011fab285f14ba441b5ff8db399c103"),
			7: sp.bls12_381_g1("0x120280eac170d6f019e7b592e717e11370ad481912768dec689a0600204dae086bdbb7dac003f36baa4bb6a5776e421a11bcde45d82721381b8e7c9df1921429304f5fb5039d6fe52bf867ea4f9fa6960312668e6bbe16e9f48664836535c2e5"),
			8: sp.bls12_381_g1("0x1320e2a2318adecf882cceef22084773171fc0d02b06feb7ce35c282f8fc33140b142b3a4e844adcf688eee00146347f0868fe7b41124363c6ab69f47fa0b1b39c2fff85c7cf3d7f0a6efdf4793bafe9716a6de09d59e835f0186d618fa1f485"),
			9: sp.bls12_381_g1("0x07b4c39d8f27ce12b1a3221817b1d5891059bfa79e54120758667722df8da907ad1c6794bddb2eca3abebaddecf18b6d160929bc103aed87d873f4aef39e05837aa85132da93f2642ffb42f85dcb9ded8362afbfc74df08a6b745d8187db4dde"),
			10: sp.bls12_381_g1("0x19ebda5eb8e6e319951dc0f61f97259fa80b80aa7c09223a81a0efec68038471f7f3fb787d90bd3bff687ab7344fd1dd007d1009a7c232cf91e5e38a18c16807fd54f94930671ff6815afaf91f269d32fa564c13395801d19418795cdd031703"),
			11: sp.bls12_381_g1("0x106b29c8d51aeb5feaa4878f1c2e0f456add414ecd4163a0c8468fed1d6a5ea5f2b412b6e46296637214bebb0933906900a31ce38b17d9281586f1ef10df3ce8326b9607c56061a89f68b485bae047eeb5842f10e683b27a386d4793dc3840c6"),
			12: sp.bls12_381_g1("0x1762670987ea7822e312842fdbb5d5b2f32301da362679eec03922996daf7dc455018763084085587d2570166bff8ced140056dbd9e8e8c97a5a90af74ad2f493bdd53fec617d05faeb98a31b24fe25fe731e6d91a9afcfd928040d155e8c426"),
			13: sp.bls12_381_g1("0x02d24b27a864481daf08ef2126a48f26fc8970c0ca7b61b7034d75e02ceb9d9d26537bd89e3262a2a63b8a32c93453901768ffd46b55dc4b781f53269677e8eaef745949f0ff35aebcb34747b2a49d3877c7825cced74d658c513fb53c496d6a"),
			14: sp.bls12_381_g1("0x11a448fe020447f70409c09cdefc3ffa4dbc1f30850f3403acd64417c52145ac39aa1dcee096581ab9976e0f4f5ed6ef09fa2e6199930486f017d74331685ca3e2799b8d5f13a7f4358fb88ffd1cb0c0b1d45e9d636005895809561bad447fec"),
			15: sp.bls12_381_g1("0x0e7accf2be10ddc47c09d77efa30c59395f63732459f25aa8719f09c7c614bc26c2861b2c98ea069d728c64797239409085414e5e0aa3eec895c1750173e289eba5e6f54a773b4af1cca2d2f27f270c1ee3d2d0cea9e20d7e4c26879bb49f429"),
			16: sp.bls12_381_g1("0x190a1ad9c04fbbfbd57f0b92d9fac08ccbdc59eb70098be6ff65c7f138de04f18485b388f0472436b3ac94b3c4ea0d3c12a89c25abe59d793d39f2b2adec6c5b78c3142dbd7311e5c53bbd3d3aac0fdb99a6a888c19a458348e69611e4984b15"),
			17: sp.bls12_381_g1("0x05512f45434b0d6ecf47bf7afea394273622bd9407682cfda50af3687737a071a1e5c6979ce3ef1a9c4bff5731171ed21790d08143463f893687519d31080753b07ee3ac583de087e66695700091398217030360683774359cb5f7a9f25df876"),
			18: sp.bls12_381_g1("0x0d15087dba422886ec26754fe07835e28be59e71bda472ab5c516cde3553275f280863e643769ce1e2a92071ef51d8b8059c48de06af1f7f4b83d62bd449fa2e4da203fe98093507c9241933a4985f913c178eaef2da33be85b9233b0cb6a03d"),
			19: sp.bls12_381_g1("0x0783ecefa49045166b487b0d957da28b5eefad37af46efbe27917c5a2aab6067cd48a3f12187ad98df09d1bfc40cab2718da50fb5276a45df83530f6b9695557a3e34ae831455dc302507f53aa36ce2f5f47eb6b697a1e3341f658141eec1019"),
			20: sp.bls12_381_g1("0x14b7285e28bbaac52d0b002792c6b5bd00de993240c922d506299b437e440db78fa8dc502d3af3272e3db2af5b5108bb0b3e63673e279121467856f307407ab2acdddb7524bdd2ebf78d20b66ba8ef9c1c957e32ef530fd6f9efa62cafd7ccde"),
			21: sp.bls12_381_g1("0x105dd52f88864e0816f6c92ae9b7f1c7f206634547a73af2484636534ac10b5ddb13b5cb1bf303ce498706204c6043d101aac566692172d56652598b2828738120cc34a573dc17e69c9bf2cda1ca9a53886eb47b4e6bfed27b5ff17283630488"),
			22: sp.bls12_381_g1("0x110f84975cf0b4b7f220dab7c1a87f6291a56bf93652cd5efd5c5e64373742f8167ddb16c6dc883813a9aca9d3ebadde0d6544f0e7b6231a731a3398b401ab67aed9ffad3b8a96ec4c4aab2ae5b06c578e41eacbebf3deb64989105a81b42cf6"),
			23: sp.bls12_381_g1("0x0e12a86559f4856874188e616c326fbf01f5999f2cbc49c5f18101af743cb42cae13fb882be1af45e03ca719417cb69005264b7f4fa399c90b2d0232def48b54939d8405a20bb171e38611fa47dfd1dc7d1579d3bc8abcbe83154117f82d81f4"),
			24: sp.bls12_381_g1("0x18fab016fbbfb8e772d340cb5d90fce479ec7536e7035e3913ca178678de14e1f8a103955cc65fb88b35568a48b9124f13c8dd9cc7101f28840d9236b4e0852d04e1070e7e80dccd302035581773479a3d8be71e0a78a4eb41289421d02a4fce"),
			25: sp.bls12_381_g1("0x110ec541768ced813db37b02a289963845b572f108ae0e0bcd0c93aa9fee45aed6877e21c96c8f1a9ad681f40a864f280f834f1161c0f022b14231dc8a53c5fe3ce258dffb3e00aef0a33bee40fddc1bfaab07ff717ad1c3ab5ecfe636a8de7c"),
			26: sp.bls12_381_g1("0x0a336e1bae638f1ddb80e77348c00777599270b9d75d5d7ef5bbed7164197134bb5bc2f13bbbd8bd308839cdc166cb330c60dd59734f96d39c7bb4d2ec2954c783ef1711af06affdc32c360453d43314666108d646fe866cc846107d3ba19d85"),
			27: sp.bls12_381_g1("0x146afa6cb8ff74505565fcb838db0efd71331383acecba85a005b9bf9c9d300f1b4a939744dd88fc1c5bff7df19b3df012cc3ac2bd7cd8d2c9d4e927e6e72cae493a0f4f15188c511f81ecb0ec93c04fdb1141f22778030fc1c1f3a72f4fa994"),
			28: sp.bls12_381_g1("0x17db9b4029d8e8d74b1f2958cf6bcb03f686d9c9b2891915930f93a2ab37a501373a0d0b55f50b3dc66a72f06b2915a90ab4120043f9a6cb931e7cc331c6d6a9b251568b2cc5e5856172d0bfd12788ab46bf1d9de52d8a6bf79c552158e980e0"),
			29: sp.bls12_381_g1("0x170f431203b6be9c1f54c1b1b080e925028bdc5a38ecb3f614b4dff3db237d9b4910a030eb6449dd7e76090396bf278f0d4700b9e869e6eb4ba83b964c137f2be5e26e046bb461fa9778db93ebff6c266c47910160cc9938ddb25d2f78b680e1"),
			30: sp.bls12_381_g1("0x1721e2644d91796e16bbe5efddf1778fff56863c74ea7cd026a5a4cfc3a10dd74f5aa389b1abbcf77ab12e5f904dbda51400c3f4b35254ab87f9c260bc7b781426c06e1a10709abb730940f2efb26e3599e6d2da8375d82519e3f3c075df63e5"),
			31: sp.bls12_381_g1("0x02b5c05d2ff4f76be5df93a01bc0d92710cfcba01023297c8af4881bcf5f24c81130f8995feacba39ef2b7fd15eddfb00ec29eb7237f79ff3fe8939deb70fbb620b28a8137f26f9b756325fe81f863706ae55857b51aadcc65e8aa8bb6db17d5"),
			32: sp.bls12_381_g1("0x0201ef1f8cc45e42f9627d943a5f0d7e8d5664750740cfd1f4a22c67a6ba85e518accfdfa9f55cd26db31bca1267ed580b8e89d67caea61cc5c0153b4b8cbd3b5ea253593693f334562838a12eea5580080bf4278127a054fbf2e3d3b436b555"),
			33: sp.bls12_381_g1("0x00ad5873b84313a15ae7ac130bc7bf9156d6424fed6211566b9acdd1f4d7c67afb960a8952b0ceea351881b71538aa890c949cb2dc8c3f3dc802d9ff28de2dec84c37ea7aa3e62d7182d869a51efd86c14a7bfade2efb86eb9cc036f7e309ffd"),
			34: sp.bls12_381_g1("0x02e5c28110dde978f7cead58ad2698c70548fcc32fd634dbef14085c8da773da6340cc243f191632d81192b1a2e9097f0679575b14e6adbd1adc526065daeebd135a320a6b2d98961eae7f4582191f68bdaeddcd5e8040d9bd1a02b69476bbaf"),
			35: sp.bls12_381_g1("0x0cd93450906f9a7389c44eb22b6ff46ffcb2f7944694c323be4b315363ec623ccfe88dfc1ee9c6dfa2743b70d7782bb8163324f7c7b9f4f6bb2d09d5afbe1a2da17ba2f63d208d43b4c663e0fbcd789c09bc982d14f67f59f48984147105333b"),
			36: sp.bls12_381_g1("0x0f779bc590144e80b0b51275865daa90eddae34603cfc67f45c7f36e25043075f8f470b8b36ccdba24b895505acfc4870bb6297b419425097421d1b89976b09b4fba316ffb670051004da8edff944566944cdf93ed8e0a47673d5b5771293897"),
			37: sp.bls12_381_g1("0x0273278d08029c4a7713eda148c1065d6b377a43aa954c71c8362d88010619da69c29794cd0becaf8115171958c344d313622968f7fbe1a4da6782ccecbeb143fe3822374ae37ebf87963deabb545375971a62c2699215c016b06a7a1d020859"),
			38: sp.bls12_381_g1("0x0b03a71dff5ef31054b60bc2217c1b04f8a574564a3aa22210ef82dc7ce8eeab9bad3ec8f0d00d12482661021827577108efa8b0d38714e337d97696509e8051e51be6dc92c16f9ca9511d924f46b43121f042d695bada84cb7f1200e9b1107e"),
			39: sp.bls12_381_g1("0x0449481309f06100bf03688ac0da1362372980eda1c4d154b4725d7860f082a5269a8c8e4afb8a871c40e6872cfaaf330af279190484667e3c4b97591451748872a13d36644453d62bc63a793ccbbbd71491a2e7d199e1f04ca1d391c7de412a"),
			40: sp.bls12_381_g1("0x0fd6a265b982b0836aba8ae3b5bdc7742253d066fa991c85c461ff07a1bcde716f901eee557c0f36900159217dadf92e134d8cf16d8f9f9d0998a397bad0a340c7a0c109e69083668a5f524bc3713e49aed41d76dd25c7d3db7b61a21c0af78c"),
			41: sp.bls12_381_g1("0x110f4ffd2635e96ef5eb1a3ee3f3b1221906ad7a9fdddcec548bd3146d949d4356321fcfb3de04b41c71eafdf446f38d062fa703b95a3306cf25d1708692e1198ad6f2e89b5b6e77eea7173755cd38589aa675db38a9d41151375e875d7d4e59"),
			42: sp.bls12_381_g1("0x07ddbfa5a93938456aab05221a43f8a3dd396b802a6b96863b8542f85c561b7b16acdb2c4a66f1bc158ae4a23bc9f10c0bb49a4385070b6d88d5af6ae7bf49b74f9894098957d36741eae59d76fa9fd29324739370a37b533986b915a218952f"),
			43: sp.bls12_381_g1("0x0ab98b45815e0abebe4327fb2a8ff3b8f2188df352bc81a501a1097bbea32ccdf156aafb6e0e3c899714d341bfe9451c0a901392e9c46c54307438e3af43989c3002ab7498ce927b18ad0cb292e0bac29e9da5a3cdb934112fb7eae805bce438"),
			44: sp.bls12_381_g1("0x18bacb23cf42e1f73d44b0fb82740f96fc0403a8ff23dde39e78206be7b16f2a91363204a34dd88991abc57f5bc1f3931028822ab7bc854d0cbda9b22a3406af33607bcc5038e98b5a1fdade8a14f465e328a4abbaf6aeab46e450151a934d0f")
		}
        
        vk_query = sp.local('vk_query', vk_query_not_local)

        vk_x_not_local  = sp.mul(vk_query.value[1], input[0]) 
        vk_x = sp.local('vk_x', vk_x_not_local)
        
        # sp.range(x, y) goes from x (inclusive) to y (exclusive)
        sp.for i in sp.range(1, sp.len(vk_query.value) - 1):
            vk_x.value = vk_x.value + sp.mul(vk_query.value[ i + 1], input[i])

        vk_x.value = vk_x.value + vk_query.value[0]     

        list_pair1 = sp.list([
            sp.pair(vk_g_alpha,vk_h_beta),
            sp.pair(vk_x.value,vk_h_gamma),
            sp.pair(proof_c,vk_h),
            sp.pair(- (proof_a+vk_g_alpha),proof_b+vk_h_beta)
        ])

        list_pair2 = sp.list([
            sp.pair(proof_a,vk_h_gamma),
            sp.pair(- vk_g_gamma,proof_b)
        ])

        check1 = sp.pairing_check(list_pair1)
        check2 = sp.pairing_check(list_pair2)
        sp.if check1 != True:
            sp.failwith("The proof is not valid, check1 failed")
        sp.if check2 != True:
            sp.failwith("The proof is not valid, check2 failed")
    
    def verify_register_execution_4_accounts(self, input, proof_a, proof_b, proof_c):
        sp.set_type(input, sp.TBigMap(sp.TInt, sp.TBls12_381_fr)) 
        
        vk_h = sp.bls12_381_g2("0x0a1ff55d377bc5d9ad20881390e9149784a166f49bd77f46c3b58e5dd1baaed7bec0704943b3a8e6e34e8ec5fecbdde70338bfb672f3e2875b13f332965a771905dcf201fa8b80cefb0c15ef61bb3faf731f2338fa6e91af460c4596b286b93002b02204273442e2d593d40f3b389d9fc7343b31bd257e7337b0c3684f3b2c09613e3f07c295e3931a562283679a0b1910fdbdd62a38c8e25a3f089257d9ebdfe3b578bd8067d91f950ed310987dc68b1ec4aee0ed88f51bce064078a9ba201c")
        vk_g_alpha = sp.bls12_381_g1("0x15cfe029e52afb3f26099db6879c7a74e21bdf415fefda77b45e0cd82646cdc4aa4b1cd3e89aff5b0a62ad0da0d079ee01f4c444d2db5b4006e86f5c37595c24187c7b7e12a9c06664ce9912f46fbe13ed6993e0005f0856d11856617381bdc9")
        vk_h_beta = sp.bls12_381_g2("0x013c38300a0a0d9a40b574782dfae2269a1aec7375f00e4927fe9d6fe81634a6293868ece4fb9508688b9020dcec221206f8e408535846ae2535b3ac61bb90f365c4932542d3e74d6c8b48ba931530a003daaa48f12d3fea10d93fe2be2c2d44174407360dccd3c7a79c32dc757a457cb928dc1845298aa3e7fae79ee227b6074e3123a78b0902737021dc95bbcfc8c803ab0ceec72f8c0850a47d0c83b8669815ff8cac3c9e4af134307335a8baf465401e30dc5c8192785766ed305bcda68e")
        vk_g_gamma = sp.bls12_381_g1("0x07e1b28d85a85e7a9f5aa098db2b2952f6950fd663877309222c6bacbb3d5ee8a51ef52b3381dbaa81d626827d045d7619350a28fa3746f9affcb591eca01b1c371fc301d19f4af366811c196e0d19804201932668a324aba0b06a5daf658845")
        vk_h_gamma = sp.bls12_381_g2("0x0a1ff55d377bc5d9ad20881390e9149784a166f49bd77f46c3b58e5dd1baaed7bec0704943b3a8e6e34e8ec5fecbdde70338bfb672f3e2875b13f332965a771905dcf201fa8b80cefb0c15ef61bb3faf731f2338fa6e91af460c4596b286b93002b02204273442e2d593d40f3b389d9fc7343b31bd257e7337b0c3684f3b2c09613e3f07c295e3931a562283679a0b1910fdbdd62a38c8e25a3f089257d9ebdfe3b578bd8067d91f950ed310987dc68b1ec4aee0ed88f51bce064078a9ba201c")
        vk_query_not_local = {
			0: sp.bls12_381_g1("0x04c9e62e122e241506c1b3082cff27209d27a4851a77b309f47d9e59f8675ec744ac5f06a8e9aa5ca9b0b557cb2d176401fcdec33baf541129996c83d05f8a3845c6ddbe9766349c831327b098800405c117cb043f847695ccdff27e40425d90"),
			1: sp.bls12_381_g1("0x0c47d2816fb5c13fb1695aa67eab0bccc0e1ce17c4eb3f07aa906f831aa5fd0e9ad8b658b656809bb75b1dcf59d75fc001905bbdd821306b2b39edbc7d83a3cfb1c26a11b47ec45ab7319f86255157be0c52ce645be8b716c8e702f8105723ff"),
			2: sp.bls12_381_g1("0x054c22d83b26c878c5b9b4a07dcc45b67255f1aa08bbcf8728446536205452cbf7157f28f14872a0ce863f0849a5a2130ff604ee64ecef7149da8cf6e7ae2e0b93b2349fc191476313127cfb1a3840782a59cfabc87ff1ad2700914e6a13ccc5"),
			3: sp.bls12_381_g1("0x1323cfebaf362457ac2112824d9b02e19ab61b38f35f88ec8a7b26e0f7a5a5ab4ed536efa2d3f975fa2afe728911d48a036bd4769651ee67deb0c2f1302ac5f3547fbab76db35c8f946274a1f6e8af6d3f116b78c5eb544337cff28ff9ae1780"),
			4: sp.bls12_381_g1("0x0e6632257764b73ea1f5c162b13db07a498c29cd57fa253236c8ef062934941747ee59a82002ec50965703558ac57ab10bd3f9c8f9612004e7d936e32fdf142d8e79849454ca5041fba261086372a81547f9011e723c6f1d4aed32c705f6958d"),
			5: sp.bls12_381_g1("0x155a3db8d4e48e0cc0dc5dfd44ea7035bfb8baa32df0cf60fbc52de995d8513017d59bd637b49c888f846940b2c5bfa8080d2b85dae77cc1a4f7c3dc261e6bbc592ca9013477b4b9a76e72574c0308623ef77e193f593ad86c1a4f141007c934"),
			6: sp.bls12_381_g1("0x06db304d091838f65fbbdedc39ba50f197e5dfbf4a9f0d9166e3bca3daf3046dc67e96118c038b4eb56ab3463e8e558a0ef35e556027ebeb66d5fb7d0e73545a65d58bcd6d5f8c140e13b582fc2aae541f344d42948db1d331e076f77fa96542"),
			7: sp.bls12_381_g1("0x0bf0efe9bfa7bc3e7bae77bef318ae62547ad41f87d56b78b713fa5cdcd7670c4316e3aee73c224b21ba0d94315496700112ef5a673fa3e5041bd15bdaa18447fedb0b15a9561fdf0b1ff953f6766f1d4418febe41653db62bcd0f4d027e0368"),
			8: sp.bls12_381_g1("0x0f11d03c2ce0738ab1e38883159f39cb7572dcce8ff2f697b6b427ce9d7c50411d60bfe2081e9d30ee2fce9ee6700c89137aa871b27fb533516481efd99fbd5a306b8be180c98fdf717d0cf8cf764690611b5cb7358c9764651f59ca26076260"),
			9: sp.bls12_381_g1("0x0bf4936fe25f19ec0f25d5725309204a7d90df42ecf10156edf54831684d52cd48f7b163588990536f29f7ebe6e8e9e801d3d7eafad39b16ba64b0205d5f4ae2080d1bf6d500119dfb79e35bbe92a683e873c1f1811171f7e9149f67c8b97e27"),
			10: sp.bls12_381_g1("0x1270ebb7b16ba92015128c52bf7c1f79876a7d53bbe9821195abe9ec888776a5e0332fe991b09464dcc4a58b9bb4c6c316b5a67f51d48be06dbdcf58edf548e7be4d0292f2dd6fc5ea7929adbe799e18ff57de390d8edf09d7c1accc2b3d916d"),
			11: sp.bls12_381_g1("0x0afeb5f87a1bfc224956297941d70532bbf1aad3b7f82dbd350618405ffa63386db905769552e9d44f864b985b0df137106f7ebcbd1b92f1555cc2eeb61715fd8cab5473c542d7679f6787ce6fe7423c3eb5531907b3b3682f4acce71015ce45"),
			12: sp.bls12_381_g1("0x0989d3814eb6fd5d352f7d3bb6fafca6e1a5afe32bc9a9fc1430315ee32aa83a68fcf8616986d23714b76c1b8c416b821518b9aac40afe4331f6fe771f1cc629e0d175df71358f16d65724d0b9b854a30e912206bcef26b2518784f7e9aa4068"),
			13: sp.bls12_381_g1("0x11b72fafe4bd2d85e4f86fc94b7464ce9bfb90f14f7c2163d0071a1fe57bbbe16951abf8fb06ea0f6be320de01eb6435030c10fb2c324b058944c2d3cb043e494a91726cd46b822fb4f8ef02b2bf80320834e2c2440cf53396c8821cabcb61df"),
			14: sp.bls12_381_g1("0x046b9ecbdaf585eee948b773dfffb91455f598b966b808ef402af225731b8280730cc0abc2458343c4cdf23830794b6308babdcc4a230dead7768b678d77f972e72f18a3b1adc9e7691a4529bdc7c5d55f771a270ac7ba95102421428022b8db"),
			15: sp.bls12_381_g1("0x105822345e3abc92e2651782ed18f95499d53ee01c738bcfb19327d244064362e84aea862672ef75dec3bd0c131f0b840cc467306c1988442a1eee0b944e06e7dcf880f5ed2435005469723d243e9e51de78ee95bbbda24b72a7b8a6a987c3e5"),
			16: sp.bls12_381_g1("0x19049fde06b3778fbde2daa16075edb819dfaa1baa18b4916fc6bc503b4d2d14560548dffc48d5a6581572b12601917e04c0292713c79e122a75b722d29ecca77ea57b4067d4c67df2bbb4a429deb1474823190c298cd1eef862c28550e9f380"),
			17: sp.bls12_381_g1("0x1974132a0a3378ddf7a97576f5f71d9e31de99ca1690f6326c90730589db063c87fdeaf104bec66fd69a64dcbc47c39917839705f4bb037ab08f324c83aa491853b11e65fe99946a1be61a2e70d02cd2a4cc641ffbbcfd2c21ca6bdd6d5f2783"),
			18: sp.bls12_381_g1("0x07a29e4550961c6e218454efabc55abdca2212df6d424fd828a5c155c7bc06714dda14b35806c749b00dd87d84e42a150757c34cce27d375dc23c4cf765c58eb18dfc0e0d256f4de0d1f3821a2c3727181e30cc9570f843c10a1869747517af8"),
			19: sp.bls12_381_g1("0x165743e9eeebc7609a5f3f050188844bedfa96493fb054b912c0ef820ba189a57120e479b4a3b9b6bfedd47f92f017c602e8064116948d5148f6bef412338abbc0628ee39384c890cdd6f1554994d2f3cd7fd06e352e5c08add14bf4180c9b6f"),
			20: sp.bls12_381_g1("0x0f993a5aae8d27266aef53b598fbbb82618665a4edb22188e6db2471d6d1bf65656860eee4796daab51dd9befee902860cc62b7caf552cf1213f5407f944fe378464b8bb4e021204813e37c67f434297f5f907b5258be54eada373e424ca5c6b"),
			21: sp.bls12_381_g1("0x11fad8986bf2607563b760777114f2fbe1ee024ba997a6b76879f58813bcb1fe15320501f33451e5b7082a7e42a3d3be0b0be4de8701166b5a25f668f1ab3a988f7939e28096ff5a1f5da2d6e9a3ec83e35801e53bf640ca4d0999604f1b0352"),
			22: sp.bls12_381_g1("0x15b236a832ab290c375cbe0cbc026cca3e3b033218af20ae6a8fde159e4b1ea17f1c59955fa84df2e31cba6683dd5bc519b0733cc139dee2515ccb6c6af691d3223ff8abb9c1af0d3e64e2975e54bb89ab80ab57fecb65736f40e1029d86951f"),
			23: sp.bls12_381_g1("0x133db520071be6a0b0502a23665f2c2712aea253113e7e54f22b532dd5cb91e03502e1bc96b1808f512fbd16e02e4ce607359b99a978b1c9e8f42207e57f574e72eb6f63bcb350067061b8a6edf052a00c9d4f66b37dd409c02a5676a300d2e6"),
			24: sp.bls12_381_g1("0x0b2f98ac98d5e40e5a3ffcbdb8d550ef71d166c49280bbfb3454f1e30ea57c430097e51b8c4affdad58148438488a51f178f2cf7e04ee7270330d5310959d292dab68b8dbf08bc47ec39a3e37169f6ba37b301359dcbf4d1677e5ba336145d32"),
			25: sp.bls12_381_g1("0x1532347325e67d6ee5d32afa164ed28e36530642c2feb83e19e04194f531cfa1f0838233d88ede87f426c171440826a5035d1a5b7ffe4d6f8b412b3e6a1868e6e00948b5307a5d3e0347910ac076669eed92e122fa220b4ccfa46cc445c4f884"),
			26: sp.bls12_381_g1("0x04fdda765f8186bf6400ca535b5dea3b58c709684fa844b0cdcb81d848f9a769fe6b14cc6ed73b087c43c12606ceb3c815bacea4ae083601b815b562b503eedf97a6ed9138945236ee4cec1685a0107aa4762dc8c3c1e37788b213c2e604d8b8"),
			27: sp.bls12_381_g1("0x077933142b3fb03fdf3049925ae04067b58d2c0e7b751ec746421a598cbe0bc2c938ae17bf45a6db770a822d27d3a1730e01a47a7e58831ef5a1461775a089179e74557cba7e217f1bfb3f43c5e3dd6dc9e39e713e46d69c10bfa7059ebbe1c7"),
			28: sp.bls12_381_g1("0x026bba8ad2552f5dfd122e6a48eaee1d2bac365ee737f98a488e69bb1df7ef9d272b636c67439f6c2eae6e26314869db191527b2887647126923ccc3a830800cc64c582e18d7da3b27f48af93d42f347368a93bbbb24426b5c64bb0e11c58adc"),
			29: sp.bls12_381_g1("0x068afa8e51d9fa352817678b7b90363bca96ed9fd2dc7c3db17b03a754b85ac689e016adf675ae9c2a59f8531f5e5dc41128ac0d5056fc47d794993d2c60a5c931b0f6203c3dd77c563c53fbf30c92f11d5bfc1ddefe969e38205ff8f0e75237"),
			30: sp.bls12_381_g1("0x09b56245cbb363f1e2329211065c6acd1a951dec63e2cc0451629e5cba19db1e9adbe0d61af4112402f3df464e3817a9002a5084601f329f81ee4a4b6c024a9e14a9aa1f148cd0517c8b7b8cd3c79b1a7eba61708989dc5d513e956f519333dd"),
			31: sp.bls12_381_g1("0x0ee68d158bfa0b5dd0025d6d8fd380f8f7f06482a84f033ab05cd776ce9aa71065bcb0e17303030acd2cedf13ef247f218aabaa513c01f3ddb48ef7ef6d193607d432fd5362412486165f490d7b8cff213708b1686ce921c0bdd360def784156"),
			32: sp.bls12_381_g1("0x0e77a906210ba4a29f883e82a54734fb19877f0f3893ac18e8de3c3cbea944d518045e6691e1a71f8e4e0227270da7c815db4d583c23e7afd8f341c9336bcb1be9997da4c22da8792a34802259e856ffec56aec66aeef223d73ba897beaa3e74"),
			33: sp.bls12_381_g1("0x10cbe40d0a4e26c1e213cb3e95abd82f3c75fd5991370ba41e791f876faa2aef935a4913297793823b31b563063aa38b0776a08c25de196fa4841c159414ceb8522c0c3e677ada31f8e5c2ee780b79ab9c622f2294847c55c106fd80c47cf52e"),
			34: sp.bls12_381_g1("0x16bc27108a00566a750f574052b308a00f53b43a97f85a997ebe2804b177cd6fc0ad8fc8250b4bf4b383de14867c6f8a0b6b2e487e93dbc69d4688be754b86b03db0c57d890709a717cbae7a0977620d687b0e45c066de2b333bf5c12aa666b1"),
			35: sp.bls12_381_g1("0x19605fefeb9b04dd191af393a595e6c15717e1bd03fee0fe2984f60f89e5f5d1a136bd3020d4157c48d25cce81f2e0a10051599d27b09d96bca99a29797b98b2f278c4226f6c02ede43e45840e306e6de4ef1d4b5563d847e5650def94977f1b"),
			36: sp.bls12_381_g1("0x19bdc8f28d8aeda65d010712167392ac9a7e1ba4cb5de2edcf0a6915a7a92ce70bb724cf4c802eb053dfb3a9d34deae60a5ed735664f64cec8f640bf42bcce8570c6d872161fa5e90ed141fe6e91e686a619e1d2dcd3389994304eba85c203c6"),
			37: sp.bls12_381_g1("0x0d8f3dbeafe72ea445ff9dd2a200135cb457263a29159e499729e928411aa1153f7ac019df62d4ab9f932b6e3436724710d615b84c06e05aa053a6119267c3d7af24c939411ab00728ea410f77d52add8bf23bebb1a85d0ebb3432f161e58d88"),
			38: sp.bls12_381_g1("0x136eee152f8bf491e9586a86738ce644ef7b65ad1c48f3c3587adbd8a4f7ca790f1a3c94aac48d6fcb8163b3db85bbdf0a1e4b0e7d1852e2e6322ee1179896f8bf6d73e1cb8a2351b861f7b614082442a911dac2e5cd79738c29bbb85f3d3da8"),
			39: sp.bls12_381_g1("0x024ecad0e89195c1d9e98768d423bcb57c878fad97ebef096e3aae0d1bd7559b7018a3db52aef2e223405a1b50602639190e04575653b948fd28eb39b739a35f2b9242b1ebe1c881a917fc175ca1ba1a5e4e094deda0a846a91f4b3ba5a2ece7"),
			40: sp.bls12_381_g1("0x01c549b263415a2dbae72a1492e252d857279ca35fb65cb36454da9f6b4a44e4fb10d22c9090e5251de4cdf24160c324041f33d15d2da4d55b5db115b305451e13f188c7beb89f43cce07d893954a6f77365afaa87f24916d0978cf20b7be062")
		}
        
        vk_query = sp.local('vk_query', vk_query_not_local)

        vk_x_not_local  = sp.mul(vk_query.value[1], input[0]) 
        vk_x = sp.local('vk_x', vk_x_not_local)
        
        # sp.range(x, y) goes from x (inclusive) to y (exclusive)
        sp.for i in sp.range(1, sp.len(vk_query.value)-1):
            vk_x.value = vk_x.value + sp.mul(vk_query.value[i+1], input[i])

        vk_x.value = vk_x.value + vk_query.value[0]     

        list_pair1 = sp.list([
            sp.pair(vk_g_alpha,vk_h_beta),
            sp.pair(vk_x.value,vk_h_gamma),
            sp.pair(proof_c,vk_h),
            sp.pair(- (proof_a+vk_g_alpha),proof_b+vk_h_beta)
        ])

        list_pair2 = sp.list([
            sp.pair(proof_a,vk_h_gamma),
            sp.pair(- vk_g_gamma,proof_b)
        ])

        check1 = sp.pairing_check(list_pair1)
        check2 = sp.pairing_check(list_pair2)
        sp.if check1 != True:
            sp.failwith("The proof is not valid, check1 failed")
        sp.if check2 != True:
            sp.failwith("The proof is not valid, check2 failed")




sp.add_compilation_target("Rollup", ZKRollupContract())