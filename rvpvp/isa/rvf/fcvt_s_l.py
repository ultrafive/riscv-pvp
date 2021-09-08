from ...isa.inst import *
import numpy as np

class Fcvt_s_l(Inst):
    name = 'fcvt.s.l'

    def golden(self):        
        return float(self['val1'])
       
