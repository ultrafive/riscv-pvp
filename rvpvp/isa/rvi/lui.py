from ...isa.inst import *


class Lui(Inst):
    name = 'lui'

    def golden(self):
        return 0