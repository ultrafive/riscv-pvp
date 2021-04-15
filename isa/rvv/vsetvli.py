from isa.inst import *

class Vsetvli(Inst):
    name = 'vsetvli'

    def golden(self):
        return 0