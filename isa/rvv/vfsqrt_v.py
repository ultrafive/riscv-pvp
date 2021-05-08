from isa.inst import *
import numpy as np

class Vfsqrt_v(Inst):
    name = 'vfsqrt.v'

    def golden(self):
        return self.masked( np.sqrt( self['vs2'] ), self['orig'] if 'orig' in self else 0 )
