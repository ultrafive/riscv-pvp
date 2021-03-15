from isa.inst import *
import numpy as np

class Metr_m(Inst):
    name = 'metr.m'

    def golden( self ):
        if 'rs1' in self.keys():
            return self['rs1'].transpose().copy(order='C')

