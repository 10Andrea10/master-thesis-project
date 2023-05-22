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
            mr_balance = {
                0: sp.bls12_381_fr("0x10D1BB3100000000000000000000000000000000000000000000000000000000"),
                1: sp.bls12_381_fr("0x1E8B414C00000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0x498955AF00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0x7D35F84500000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0x5DE55AE900000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0x0A94C5CF00000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0x2C6B905D00000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0x1A5DD67400000000000000000000000000000000000000000000000000000000"),
                },
            mr_nonce = {
                0: sp.bls12_381_fr("0x7B6CC91700000000000000000000000000000000000000000000000000000000"),
                1: sp.bls12_381_fr("0x802628F400000000000000000000000000000000000000000000000000000000"),
                2: sp.bls12_381_fr("0x95228D5E00000000000000000000000000000000000000000000000000000000"),
                3: sp.bls12_381_fr("0xB1D379D300000000000000000000000000000000000000000000000000000000"),
                4: sp.bls12_381_fr("0x0628B1EA00000000000000000000000000000000000000000000000000000000"),
                5: sp.bls12_381_fr("0xEEFE904C00000000000000000000000000000000000000000000000000000000"),
                6: sp.bls12_381_fr("0x160B367200000000000000000000000000000000000000000000000000000000"),
                7: sp.bls12_381_fr("0xBDD51BBE00000000000000000000000000000000000000000000000000000000"),
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
            sp.verify(sp.to_int(self.data.mr_balance.get(i-8)) == sp.to_int(params.received_values.get(i)))

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
            sp.verify(sp.to_int(self.data.mr_balance.get(i-8)) == sp.to_int(params.received_values.get(i)))
        
        # TODO: put an if on the number of accounts passed as parameter and call the correct function
        self.register_new_with_4_accounts(params)



                
    def rollup_with_4_accounts(self, params):
        # The verify function is called.
        self.verify_rollup_execution_4_accounts(params.received_values, params.received_proof_1, params.received_proof_2, params.received_proof_3)

        # TODO: check if the index is correct
        pos_first_balance_in_received_values = sp.local('pos_first_balance_in_received_values', sp.int(32))
        pos_first_nonce_in_received_values = sp.local('pos_first_nonce_in_received_values', sp.int(36))
        sp.for i in sp.range(0, sp.as_nat(4)):
            # Conversions explanation:
            # - sp.utils.nat_to_mutez(sp.as_nat(sp.to_int( is because we're receiving types of sp.TBls12_381_fr and we need to convert them to mutez
            # - sp.to_int(i) is because the sp.range wanted a nat but to access a map we need an int, idk why since it's a big map declared with tkey = sp.TNat
            self.data.accounts[i].mutez_balance = sp.utils.nat_to_mutez(sp.as_nat(sp.to_int(params.received_values[ sp.to_int(i) + pos_first_balance_in_received_values.value])))
            self.data.accounts[i].nonce = sp.as_nat(sp.to_int(params.received_values[ sp.to_int(i) + pos_first_nonce_in_received_values.value]))
            self.data.last_rollup_timestamp = sp.timestamp_from_utc_now()
    

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
        
        vk_h = sp.bls12_381_g2("0x19b0a2b6b8bebe3229870144936f1979ad3f6a7845c70de0268fa32c8730b8a560b2aeb729252746fc97a1049eba19701435dd487f28284ef9c3e6fd0150a5f478aae88eb0695be36d754783871f2d6b4fd67f8cf13bfb217dacdc886a2d5d8e08a0727cef51fc401d8c23323ff619470721f2544cc3ed5dd2c6cb06d2ac8c14d129c26e833ef2f7342c7c6f99f6d93004a9f85f4d58edadecffa31bb2f267c1bea28db600acae84861a1902b49ad96639124c8f0a14a6e4e684159abe8b2a9d")
        vk_g_alpha = sp.bls12_381_g1("0x0e239554f22a9943f07bf2daca9ed94b05758b817c35709763b2ce88982bd4f46ac4f2cbd6feb0e16d16f92a3f0a4a840cdea4e95ba6c439f7115ec670cdfec01bcafda11cdc1b75fcf0597fe140f39546e39c8f9a1df8c0505a250d19e22ba8")
        vk_h_beta = sp.bls12_381_g2("0x175a76b0996239d2ca7147fe2e203d9b448c9e31607d4afe9df7d60b12987256bf180941f3f4729838ce25d8c03c968d098d60a1a1967504f5a5a68d5ae524df7c08f545d694719c5dfdc99b78c3323831ba8d6409a92b8634b49022805f405a0fc9d8137145491258c0c496a0d9e3124f3a066c82f2dc79a4eb9744c4bc9ca48cf7946fb1dd2caa2e21d1797541f6300b1a0b691c3626a650334d1d7f62d10dc182a6b62b5aca3189cc454602a0ff831f5f43cc4ebfcb3c86318eb73116ac2d")
        vk_g_gamma = sp.bls12_381_g1("0x15de91c3d82427b42d55d890816b25342e8fa2375ad33333e389a997dbda68cf9519ca50da73f2570ce2e8b23d6aec7d12c29fb6a4c20e2c2a959b0e2588aee902e2643de6d07460e78184a5bdd3c4ce35467b472d3646692c4501099c937e58")
        vk_h_gamma = sp.bls12_381_g2("0x19b0a2b6b8bebe3229870144936f1979ad3f6a7845c70de0268fa32c8730b8a560b2aeb729252746fc97a1049eba19701435dd487f28284ef9c3e6fd0150a5f478aae88eb0695be36d754783871f2d6b4fd67f8cf13bfb217dacdc886a2d5d8e08a0727cef51fc401d8c23323ff619470721f2544cc3ed5dd2c6cb06d2ac8c14d129c26e833ef2f7342c7c6f99f6d93004a9f85f4d58edadecffa31bb2f267c1bea28db600acae84861a1902b49ad96639124c8f0a14a6e4e684159abe8b2a9d")
        vk_query_not_local = {
			0: sp.bls12_381_g1("0x0e3937d81f8a1169d022f225a189c78addd0c16dd0346f2b8232d931f01ce306be4401453bcd248e874235e407485962138dda7116c8b5ab8c69710bb4b4ec8cbb835e48bd636f8f52d9c1a1e976df68dbbc7149c00e18e8d5e76a88fadf1ac3"),
			1: sp.bls12_381_g1("0x03d1f23cae2e4e6faf0a4df37d61d0fe994f58edf4d4583886ae7ff8bdda6ef725311df836eeaa8098f179a17b58d34713e47cd18f6d432f8178ecb2ae5714485ab9177ce1a07017b11f294ef235455c5feda9ab4ad9253a4453a42b2213bdb8"),
			2: sp.bls12_381_g1("0x0f937c847e46d3e288564a1aa1f514b80db4b1c9b0d3421db9b4ba5416352615f2d4460febf8f750a9edd652ee92f4281095c98c64338768f4bfac3e9a621e7ce035983ef1f2eec317c414375443a6c35b807b7b2b43832a413cf881196ec6ef"),
			3: sp.bls12_381_g1("0x0ed24732e72680cac003572cf7c0b95504958fc9027db052823d64edd247cd05600c24d694122226e79f9f0ed46d0091144ff0b360028ebe540f98defc5c66ddd0bc6cf555869a37ba5cf10c90f98e7c7a1ffe49e0a07d9b49757e33f072accf"),
			4: sp.bls12_381_g1("0x02cf9c48f68a4b6a121b24f6851b1da3ebd4aee198fbcef774ad9c4bbff9f58012361d83c7273fc8c29803fdcc3129d30d2e1148fc5759958d7b35dde48e0666d7315849a5f15ae1d46948e40e4b4fa74944f9473ab1bc396334256249199535"),
			5: sp.bls12_381_g1("0x04da638b08062c323d73cc113eef28af5cae2238f66f7bae35cc7f40e61598f5ba45325d663e05ade8cd67f3fe23500f0483f465223b81282b04ac376c4d9e32133c4ecfc58ae9d9e1460327a809785f23bde4d8cfffbde641ce813e5e454ffa"),
			6: sp.bls12_381_g1("0x024a310f90bf8f58787681f3aeb160dc0bd53e8c98fb1d6ec5831ca0b1501ccf24da34bb0cfb098b1703afd4900f83320abbb7f0f7adc19246456d09b50bbc759d91dcd3ee58cab2b9ac7390d39358c95be80efe475773129bf47e51f7533700"),
			7: sp.bls12_381_g1("0x0defab33f13737dbab87075da7603d445558425bfde72793f3c8f19c6fd8de974a12105dfb661d50c8698993e55b30e401f2547abd0619a00c0afa37ca7ff66f259cbd2f0cedafd769c8ed77a4a988fd504a1756820deb9dd9f5b67cfded96f1"),
			8: sp.bls12_381_g1("0x00bbe32a7c0b2ac8061c7a5816d99748a1b6822bf0dfff8dae7453e16560b51be7da07763ea763c9b935b2fd2a7b9cd316b32d5e9f0906283614701df5537f0b1531b7e89ed090c264229e1d423970738c9fe10f7bb03e074c682a314b937810"),
			9: sp.bls12_381_g1("0x120d79316e3d83d81b0dfb70a69b9cdf6473ffee7c1df023fd34f138e0ca850fe1bde142e62e8887c30b70fb0817d13909fc748ca6dcab07e64e3855537ead493e8db40e626f2f98c23abbf5860852401c8d657f7af824c7111113b1b8d464d8"),
			10: sp.bls12_381_g1("0x0cfed15e4afda0430a05b5f1a17b9ea4206df08246cfc3effd3cfdc71996aa1def368b1df0e61cb42830d30fc61a89470b2ea65ad8d8a8a9c2ae56fb5c614b1dc9391fb13477215064b223258ba33ef2271a14215a65bfe5388a48342289b8b9"),
			11: sp.bls12_381_g1("0x0a3ffd266aafb5033e1838c2f930e1abb6c6729413212270e4b09cb7e1a631c98a78e61f730e1f8424740ecd3312f32d1561355904ea5e963a0c8fef846a696f7d06741ae29d5ec466d2619e3302cfb812bde7df231f047d3eb5d76c32830d70"),
			12: sp.bls12_381_g1("0x0488f68aa40da9fcc3ec159225496d777d1e781005ad603218260e41ee9368b8cabdd8980505990884f5b72b7cef74d30e9303cfae86e8045c24de1d6324b885accc2090ff12d6c408b3acec06cd8fbb074f8b8afcd0d6ac64815a4114c6f479"),
			13: sp.bls12_381_g1("0x0cbc8e215a72441178efe01621ae97fef749bd6b1632779e866e5f669891f33bc342b380ba209081425612070b644005102d1770fb00167f2f5362d5f91afcbde2fb7661742e8594e9e009f5925baea52138900fd4ea03885f523ab5427dbf61"),
			14: sp.bls12_381_g1("0x11bc79e3bb76a12040883b8308cc214b3164061a8fe81d27db2ac1b72d38b23eaf231772843dfdac0c59700ad8bce777106ba89ee7386a6c5062ea36226e7de527ceda3a0ebf9306d8af8496fec1582bbd0b2ab02067e94e40f551f33bc02b4e"),
			15: sp.bls12_381_g1("0x05fe66a130eb7ecb8fc884497580382697994190941a999f38f8c57714d96cb4a2ace15fcc21cab5093d4c1542afa6b41071566e121352b2140888c24aca9eba5ffcd5bb9f0394af81c1736b6591b3831785b1900a7343d7cad90d43bfbde6ab"),
			16: sp.bls12_381_g1("0x00bbcb130a6db18905edf7c3ee65727b8273881ad72c144d73f567c4c6a47401887760b769e6db2f179bc0f5c0b122950a8243d75123e9f88f4497bc8b95ec6c6bd151aa58e8ff9735b62a7c1728d31c54b1ac7afd21f7766e9fa78ce6c25f8f"),
			17: sp.bls12_381_g1("0x0c3eadb12917ad75cfb3bc0984cb50ea704338fde321b8a51563d52b4c966e9dc99c71951552db805cb57942d4016a7d0e4784261af166072a239b96669a51419d879e5f5fb4558cd085831e4bb3c7bec9ed89ddddd0da80035de0dd19dc5920"),
			18: sp.bls12_381_g1("0x042d6f79384d54ed875b1d1e045428ed70e83163681378c90c3f424f0eaf0b142de2733a3b9d0ff17948610bcccf1c0d12328e8f6ab32f91dddf57036bfdb544d4e4bd84937e3c0f94c31e5ca0179de96c435f940fd5a1effea4d291e38c46bc"),
			19: sp.bls12_381_g1("0x06f190242ad0e25752cd79f4da984cfc19bd1e17943dada9fed22c7f049b13957fd7214d91eb3f9884c9457ef53bce1707e2dee0a9bfd9788e7681472eaeae861f36772bc69dfaae6e1dcf5919da40769f221389fcb60519f510a9c1adbc5179"),
			20: sp.bls12_381_g1("0x193aeb71dd1e34849aafab7a8097a9e6d22d4d27b39b615bbb346ecc64e65befa7f0bc9b97a4e5d4309463ef4f8fe754048d5b72cfa4e6ace49b57d6c8f23202e1146d7863ae4d670f59a4ea6c741302e2faa4d8dba0d42e4f111bda04d7851c"),
			21: sp.bls12_381_g1("0x0e94b243a6fc5645800abcf765c5e2b726535d77e0a3c3dcfd6c4cd5bc668d65e5f887d67ca4fa31342259229c2fb87f164e7aee268a1265132a72dade222da6e2b3253ddcf624a302a050e5a03d6749e805b6a64d4786ecae804961566ecff1"),
			22: sp.bls12_381_g1("0x0119373ec71c030f6424c8b57b7d793885731048866edda61eeb6a088f53ec34d61019c8cbf031d550a387722fdc405200960bed85cb94ec30e4fbda0127725bd97b669030e925df321c30c53efd9cb177174c91f2df069df684452bf92060a5"),
			23: sp.bls12_381_g1("0x0d109717777be6aea630370e21406d7cc0291084ebb64beb038199ae20987ba595870a3bd1848dc95d29adb5c221f12704aa6e14e109ecad20b95f8b9facd0866c1b7afb3ace3e09cac1755293574ec4337909b7ef6aebdc308142a40a6f7c6d"),
			24: sp.bls12_381_g1("0x16cd8c3a04248965a7fd1063033206c2c67543b1ef631e489ca77b9bbf50ea40c9f7702fc9b808be937dbdc4f0b6a4d9165e2c48fc368de129823c000814a96aa089fe57c2be2abaea34607d205ed19c2cf606e7f03f2888f2d3598ee459b98d"),
			25: sp.bls12_381_g1("0x0b0c231cfc6fd248c2f629d7c329d1de601b691a49391a2ad94c108a6c6a2c50c246f7a9dbdb5a160c2275357ec966f802a22343273b79d70db9c1dd935bee888abb17b38db6a3f530baf47e86e935fbfacee03ce93d519a784228910aaa6438"),
			26: sp.bls12_381_g1("0x16caf27835968d49df0d53f3d8221834911aab34023b4c8efab4e436fb3c14f252816c5a1e85e18304abd016c46395470f04e03a29d63c142689ed95cd2bf2559b30b38c4cca33420df780001a42765fb634a7202f0916514ca014891e53e5f5"),
			27: sp.bls12_381_g1("0x0e5cf5e337266b99413f53bcb1b7458469a0dfee49476f6e25c9828e47ec496972e868a30f5de2b0c458af6003d7e12b0acddf97b32617a4376b8c28f6fb3f59737e833be259ef65a52e1ed3b0791b9d7d60733a7614404619db2b0f79a4b782"),
			28: sp.bls12_381_g1("0x1761d5e0bf04e4c5a829cae4fedb46edae5743fbb217499beeccf8bb278566ff66337ac5d8f1e2b284b6a79ba034725d092a3440f09a6b40d2317539bc702c71a69d7d85f8026afac0a44ca48e905e752993c1170bbadcf32050208c46222975")
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

        # TODO: check if this is correct, I removed the check1 and check2 from the contract storage
        check1 = sp.pairing_check(list_pair1)
        check2 = sp.pairing_check(list_pair2)
        sp.if check1 & check2 != True:
            sp.failwith("The proof is not valid")
    
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

        # TODO: check if this is correct, I removed the check1 and check2 from the contract storage
        check1 = sp.pairing_check(list_pair1)
        check2 = sp.pairing_check(list_pair2)
        sp.if check1 & check2 != True:
            sp.failwith("The proof is not valid")


sp.add_compilation_target("Rollup", ZKRollupContract())