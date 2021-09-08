from ...isa.inst import *


class Auipc(Inst):
    name = 'auipc'

    def golden(self):
        return 0