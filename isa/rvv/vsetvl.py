from isa.inst import *

class Vsetvl(Inst):
    name = 'vsetvl'

    def golden(self):
        return 0