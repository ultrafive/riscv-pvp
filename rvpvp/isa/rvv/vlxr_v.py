from ...isa.inst import *
import math

class Vlxrx_v(Inst):
    name = 'vlxrx.v'
    def golden(self):
        res = np.zeros(self['VLEN']*8//self['eew'], dtype=self['rs1'].dtype)
        vlen = self['nf']*self['VLEN'] // self['eew']
        start = self['start'] if 'start' in self else 0
        if start < vlen :
            res[start: vlen] = self['rs1'][start: vlen]
        return res
    

  

