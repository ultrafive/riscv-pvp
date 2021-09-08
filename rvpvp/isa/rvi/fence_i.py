from ...isa.inst import *

class Fence_i(Inst):
    name = 'fence.i'

    def golden(self):
        return 0
