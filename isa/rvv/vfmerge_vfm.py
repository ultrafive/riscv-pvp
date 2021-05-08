from isa.inst import *
import numpy as np

class Vfmerge_vfm(Inst):
    name = 'vfmerge.vfm'

    def golden(self):

        return self.masked( self['rs1'].astype( self['vs2'].dtype ), self['vs2'] )
