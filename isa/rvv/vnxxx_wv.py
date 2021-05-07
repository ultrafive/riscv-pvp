from isa.inst import *
import numpy as np

class _vnxxx_wv(Inst):
    def golden(self):
        vd = self['vs2'] >> self['vs1']
        if self['vs2'].dtype == 'uint64':
            vd = vd.astype(np.uint32)
            vd.dtype = 'uint32'
        elif self['vs2'].dtype == 'int64':
            vd = vd.astype(np.int32)
            vd.dtype = 'int32'
        elif self['vs2'].dtype == 'uint32':
            vd = vd.astype(np.uint16)
            vd.dtype = 'uint16'
        elif self['vs2'].dtype == 'int32':
            vd = vd.astype(np.int16)
            vd.dtype = 'int16'
        elif self['vs2'].dtype == 'uint16':
            vd = vd.astype(np.uint8)
            vd.dtype = 'uint8'
        else:
            vd = vd.astype(np.int8)
            vd.dtype = 'int8'

        return self.masked(vd)

class Vnsrl_wv(_vnxxx_wv):
    name = 'vnsrl.wv'

class Vnsra_wv(_vnxxx_wv):
    name = 'vnsra.wv'
