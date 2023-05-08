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
    The main entry point of the contract.

    It receives a proof from the client and checks if it is valid.
    - The output values are in params with the name received_values.
    - The 3 proofs are in params with the name received_proof_1, received_proof_2 and received_proof_3.
    - The amount of accounts stored is in params with the name of NUMBER_OF_ACCOUNTS. It is necessary
        as the contract cannot iterate over a Big Map but an external service using an rpc can. And
        it will be used in future to support a variable number of accounts.
    """
    @sp.entry_point
    def receive_proof(self, params):

        # Check if the current mr_pub_key is the same as the one received in the proof
        sp.for i in sp.range(0, 8):
            sp.verify(sp.to_int(self.data.mr_pub_key[i]) == sp.to_int(params.received_values[i]))
        
        # Check if the current mr_balance is the same as the one received in the proof
        sp.for i in sp.range(8, 16):
            sp.verify(sp.to_int(self.data.mr_balance.get(i-8)) == sp.to_int(params.received_values.get(i)))

        # Check if the current mr_nonce is the same as the one received in the proof
        sp.for i in sp.range(16, 24):
            sp.verify(sp.to_int(self.data.mr_nonce.get(i-16)) == sp.to_int(params.received_values.get(i)))

        # TODO: put an if on the number of accounts passed as parameter and call the correct function
        self.rollup_with_4_accounts(params)

        
                
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



sp.add_compilation_target("Rollup", ZKRollupContract())