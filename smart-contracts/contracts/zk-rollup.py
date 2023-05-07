import smartpy as sp
class ZKRollupContract(sp.Contract):
    def __init__(self):
        self.init(
            last_rollup_verified = False,
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

    @sp.entry_point
    def okay(self):
        self.data.last_rollup_verified = True


sp.add_compilation_target("Rollup", ZKRollupContract())