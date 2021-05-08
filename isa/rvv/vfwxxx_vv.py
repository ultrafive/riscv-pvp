from isa.inst import *
import numpy as np

class Vfwadd_vv(Inst):
    name = 'vfwadd.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs1'].astype( dtype_vd ) + self['vs2'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )

class Vfwsub_vv(Inst):
    name = 'vfwsub.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs2'].astype( dtype_vd ) - self['vs1'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )

class Vfwmul_vv(Inst):
    name = 'vfwmul.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )           

