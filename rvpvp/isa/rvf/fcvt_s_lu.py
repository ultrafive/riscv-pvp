from ...isa.inst import *
import numpy as np

class Fcvt_s_lu(Inst):
    name = 'fcvt.s.lu'

    def golden(self):        
        val1 = int(np.array([self['val1']],dtype=np.int64).byteswap().tobytes().hex(), 16)
        return float(val1)
       
