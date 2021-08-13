from isa.inst import *
import numpy as np
import math

class Vlexff_v(Inst):
    name = 'vlexff.v'

    def golden(self): 
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(self['vl'], dtype=self['rs1'].dtype)
        if 'start' in self:
            start = self['start']
        else:
            start = 0
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(self['vl'], dtype=self['rs1'].dtype)

        end = self['nvl'] if 'nvl' in self else self['vl']

        if 'offset' in self:
            rs1 = self['rs1'].copy()
            rs1.dtype = np.uint8
            mul = self['rs1'].itemsize // rs1.itemsize
            rs1[0: (self['vl']*mul-self['offset'])] = rs1[self['offset'] : self['vl']*mul]
            rs1[(self['vl']*mul-self['offset']): self['vl']*mul] = 0
            rs1.dtype = self['rs1'].dtype
        else:
            rs1 = self['rs1'].copy()

        res = self.masked(rs1, origin[0: self['vl']])
        origin[start: end] = res[start: end]
         
        return origin

                       