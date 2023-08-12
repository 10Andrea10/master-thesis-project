import smartpy as sp
class Ajeje(sp.Contract):
    def __init__(self):
        self.init(
            current_size = sp.nat(0),
        )
    
    @sp.entry_point
    def add_partial_vk(self, params):
        sp.set_type(params.sizeInput, sp.TNat)
        self.data.current_size = params.sizeInput
        
        
sp.add_compilation_target("Ajeje", Ajeje())
