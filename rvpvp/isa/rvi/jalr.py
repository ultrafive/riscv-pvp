from ...isa.inst import *

class Jalr(Inst):
    name = 'jalr'

    def golden(self):
        return 0
