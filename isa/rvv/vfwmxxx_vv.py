from isa.inst import *
import numpy as np

class Vfwmacc_vv(Inst):
    name = 'vfwmacc.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64    
        return self.masked( self['vs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ) + self['vd'], self['vd'] )    

class Vfwnmacc_vv(Inst):
    name = 'vfwnmacc.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64  
        return self.masked( - ( self['vs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ) ) - self['vd'], self['vd'] )      

class Vfwmsac_vv(Inst):
    name = 'vfwmsac.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64        
        return self.masked( self['vs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ) - self['vd'], self['vd'] )

class Vfwnmsac_vv(Inst):
    name = 'vfwnmsac.vv'

    def golden(self):
        dtype_vs = self['vs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64        
        return self.masked( -( self['vs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ) ) + self['vd'], self['vd'] )                                  
