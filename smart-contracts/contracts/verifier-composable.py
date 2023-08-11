import smartpy as sp
class VerifierComposable(sp.Contract):
    def __init__(self):
        self.init(
            vk_query = sp.big_map(
                l = {},
                tkey = sp.TNat,
                tvalue = sp.TBls12_381_g1
            ),
            current_size = sp.nat(0),
        )
    
    @sp.entry_point
    def add_partial_vk(self, params):
        sp.set_type(params.input, sp.TBigMap(sp.TNat, sp.TBls12_381_g1))
        sp.set_type(params.sizeInput, sp.TNat)
        sp.for i in sp.range(self.data.current_size, self.data.current_size + params.sizeInput):
            self.data.vk_query[self.data.current_size + i] = params.input[i]
        self.data.current_size += params.sizeInput
    
    @sp.entry_point
    def verify(self, params):
        sp.set_type(params.input, sp.TBigMap(sp.TInt, sp.TBls12_381_fr))

        vk_h = sp.bls12_381_g2("0x0866b3d155dfe7072d9ef35ee0fa067e1e39a8a8de32b012285462340475ae4995b2d6c3b4856fdf2617a49d2bace5a515e354b9a3fa4f1a507fcea871854b4abc38cc82ef55f10c9358e0023ddbecc638bb37f4b0f2070f52994c9709ed802d119b9695938d40b1a53a4bb3e38841bb06c123610d2a8a1667f29788b4766fde5bb378f8e17f7cdb15b29ecf4722ef50044a7f3227a4adefc11772aa055a07baecd83bf8b7d69073c30b68ae5feb40b9a81053bb2f6d267f8b654264bbe5d4e0")
        vk_g_alpha = sp.bls12_381_g1("0x10a485b19895f5ddc7b212c9e888887b603127bf99e7f28e6c11e834ef2192846667b72bac427b0384d6cb6b831b0f160ad7672a30795b0a982968a252b569e83ef1c95c98b47aae8c1584d58a84478f0c40c8454736c56e1236affae8d0a689")
        vk_h_beta = sp.bls12_381_g2("0x1100fd8fa50fc708206aebfc62eb2f385819194c2edf5844b4cbc8d0237991ec01e2840c2f55be0b4aa5da0797a6a95c0dd3e89007e9418a8f2965dca5f6ab68f7515f3456f7d42fb151006792fbca920c1ae27328cf6eb15ecaa55e4e6368ad057856fcb6705e26fe1ddf75985497b64ac5e91786328b7042a63bbbe809877f56e6cb45124b6c6636a03aa219784a7a11fc24fbdcb484757f60972fe30875a3f0d29371b2fa6770b71b33c796d8b52b1bd034cf43b8d038784fb4f3101e4392")
        vk_g_gamma = sp.bls12_381_g1("0x027c085d09cc7c6609db47380417d55d7dc5a447b60b7c9b82a0b13efcef2d5376931c3ac50f5c7feb2e3a54316ec4db071b4d11679c3b97177f3f13a99eb799712567f8131551ec8682a918ad767c3eaea5e7d8b5984f33f7e1ca67fac5486d")
        vk_h_gamma = sp.bls12_381_g2("0x0866b3d155dfe7072d9ef35ee0fa067e1e39a8a8de32b012285462340475ae4995b2d6c3b4856fdf2617a49d2bace5a515e354b9a3fa4f1a507fcea871854b4abc38cc82ef55f10c9358e0023ddbecc638bb37f4b0f2070f52994c9709ed802d119b9695938d40b1a53a4bb3e38841bb06c123610d2a8a1667f29788b4766fde5bb378f8e17f7cdb15b29ecf4722ef50044a7f3227a4adefc11772aa055a07baecd83bf8b7d69073c30b68ae5feb40b9a81053bb2f6d267f8b654264bbe5d4e0")
        
        vk_x_not_local  = sp.mul(self.data.vk_query[1], params.input[0]) 
        
        vk_x = sp.local('vk_x', vk_x_not_local)
        
        # sp.range(x, y) goes from x (inclusive) to y (exclusive)
        sp.for i in sp.range(1, self.data.current_size - 1):
            vk_x.value = vk_x.value + sp.mul(self.data.vk_query[ sp.as_nat(i + 1)], params.input[i])

        vk_x.value = vk_x.value + self.data.vk_query[0]     

        list_pair1 = sp.list([
            sp.pair(vk_g_alpha,vk_h_beta),
            sp.pair(vk_x.value,vk_h_gamma),
            sp.pair(params.proof_c,vk_h),
            sp.pair(- (params.proof_a+vk_g_alpha),params.proof_b+vk_h_beta)
        ])

        list_pair2 = sp.list([
            sp.pair(params.proof_a,vk_h_gamma),
            sp.pair(- vk_g_gamma,params.proof_b)
        ])

        check1 = sp.pairing_check(list_pair1)
        check2 = sp.pairing_check(list_pair2)
        sp.if check1 != True:
            sp.failwith("The proof is not valid, check1 failed")
        sp.if check2 != True:
            sp.failwith("The proof is not valid, check2 failed")


sp.add_compilation_target("VerifierComposable", VerifierComposable())
