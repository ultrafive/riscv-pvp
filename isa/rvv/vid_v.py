from isa.inst import *
import numpy as np
import math

class Vid_v(Inst):
    name = 'vid.v'

    def golden(self):
        return np.arange(self['vlen']).astype('uint'+str(self['ebits']))