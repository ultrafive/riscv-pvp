from isa.inst import *
import numpy as np

class Vfwadd_wv(Inst):
    name = 'vfwadd.wv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs1'].astype( dtype_vd ) + self['vs2'], self['orig'] if 'orig' in self else 0 )

class Vfwsub_wv(Inst):
    name = 'vfwsub.wv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs2'] - self['vs1'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )           
