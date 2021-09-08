from ...isa.inst import *
import numpy as np

class Fcvt_s_w(Inst):
    name = 'fcvt.s.w'

    def golden(self):        
        return float(self['val1'])
       
