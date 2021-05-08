from isa.inst import *
import numpy as np

class Vfwmacc_vf(Inst):
    name = 'vfwmacc.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64  

        return self.masked( self['vs2'].astype( dtype_vd ) * self['rs1'].astype( dtype_vd ) + self['vd'], self['vd'] )       

class Vfwnmacc_vf(Inst):
    name = 'vfwnmacc.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64 

        return self.masked( - ( self['vs2'].astype( dtype_vd ) * self['rs1'].astype( dtype_vd ) ) - self['vd'], self['vd'] )                    


class Vfwmsac_vf(Inst):
    name = 'vfwmsac.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64         
        return self.masked( self['vs2'].astype( dtype_vd ) * self['rs1'].astype( dtype_vd ) - self['vd'], self['vd'] )


class Vfwnmsac_vf(Inst):
    name = 'vfwnmsac.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64         
        return self.masked( - ( self['vs2'].astype( dtype_vd ) * self['rs1'].astype( dtype_vd ) ) + self['vd'], self['vd'] )          

