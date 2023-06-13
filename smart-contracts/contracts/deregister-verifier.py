import smartpy as sp
class DeregisterVerifier(sp.Contract):
    
    @sp.entry_point
    def verify_deregister_4(self, params):
        sp.set_type(params.input, sp.TBigMap(sp.TInt, sp.TBls12_381_fr))
        
		# TODO: insert verificationkey
        
        vk_query = sp.local('vk_query', vk_query_not_local)

        vk_x_not_local  = sp.mul(vk_query.value[1], params.input[0]) 
        vk_x = sp.local('vk_x', vk_x_not_local)
        
        # sp.range(x, y) goes from x (inclusive) to y (exclusive)
        sp.for i in sp.range(1, sp.len(vk_query.value) - 1):
            vk_x.value = vk_x.value + sp.mul(vk_query.value[ i + 1], params.input[i])

        vk_x.value = vk_x.value + vk_query.value[0]     

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

sp.add_compilation_target("DeregisterVerifier", DeregisterVerifier())
