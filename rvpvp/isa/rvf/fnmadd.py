from ...isa.inst import *
import numpy as np

class Fnmadd(Inst):
    name = 'fnmadd.s'

    def golden(self):
        return -self['rs1']*self['rs2']-self['rs3']
       
