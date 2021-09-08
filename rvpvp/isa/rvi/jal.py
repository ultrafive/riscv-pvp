from ...isa.inst import *

class Jal(Inst):
    name = 'jal'

    def golden(self):
        return 0
