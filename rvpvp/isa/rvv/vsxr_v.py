from ...isa.inst import *
import math

class Vsxr_v(Inst):
    name = 'vsxr.v'
    def golden(self):
        res = np.zeros(self['VLEN']*8//8, dtype=np.uint8)
        vlen = self['nf']*self['VLEN'] // 8
        start = self['start'] if 'start' in self else 0
        if start < vlen :
            res[start: vlen] = self['vs3'][start: vlen]
        return res
    
          