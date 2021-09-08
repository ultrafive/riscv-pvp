from ...isa.inst import *
import numpy as np

class Fmsub(Inst):
    name = 'fmsub.s'

    def golden(self):
        return self['rs1']*self['rs2']-self['rs3']
       
