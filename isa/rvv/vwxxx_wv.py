from isa.inst import *
import numpy as np

class Vwaddu_wv(Inst):
    name = 'vwaddu.wv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) + self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) + self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) + self['vs1']
        
        return self.masked(vd)

class Vwadd_wv(Inst):
    name = 'vwadd.wv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) + self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) + self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) + self['vs1']
        
        return self.masked(vd)

class Vwsubu_wv(Inst):
    name = 'vwsubu.wv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) - self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) - self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) - self['vs1']
        
        return self.masked(vd)

class Vwsub_wv(Inst):
    name = 'vwsub.wv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) - self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) - self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) - self['vs1']
        
        return self.masked(vd)