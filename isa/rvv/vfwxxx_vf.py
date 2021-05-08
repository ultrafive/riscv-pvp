from isa.inst import *
import numpy as np

class Vfwadd_vf(Inst):
    name = 'vfwadd.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['rs1'].astype( dtype_vd ) + self['vs2'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )


class Vfwsub_vf(Inst):
    name = 'vfwsub.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['vs2'].astype( dtype_vd ) - self['rs1'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )

class Vfwmul_vf(Inst):
    name = 'vfwmul.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        return self.masked( self['rs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ), self['orig'] if 'orig' in self else 0 )

