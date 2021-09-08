from ...isa.inst import *
import numpy as np

class Fcvt_s_wu(Inst):
    name = 'fcvt.s.wu'

    def golden(self):        
        val1 = int(np.array([self['val1']],dtype=np.int32).byteswap().tobytes().hex(), 16)
        return float(val1)
       
