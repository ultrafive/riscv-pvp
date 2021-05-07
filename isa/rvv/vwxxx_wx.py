from isa.inst import *
import numpy as np

class Vwaddu_wx(Inst):
    name = 'vwaddu.wx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) + self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) + self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) + self['rs1']

        return self.masked(vd)

class Vwadd_wx(Inst):
    name = 'vwadd.wx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) + self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) + self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) + self['rs1']
        
        return self.masked(vd)

class Vwsubu_wx(Inst):
    name = 'vwsubu.wx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) - self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) - self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) - self['rs1']
        
        return self.masked(vd)

class Vwsub_wx(Inst):
    name = 'vwsub.wx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) - self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) - self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) - self['rs1']
        
        return self.masked(vd)