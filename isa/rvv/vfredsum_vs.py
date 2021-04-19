from isa.inst import *
import numpy as np

class Vfredsum_vs(Inst):
    name = 'vfredsum.vs'

    def golden(self):
        if 'rs2' not in self and 'orig' in self and 'rs1' in self:
            self['orig'][0] = self['rs1'][0] + self['rs1'].sum()
            return  self['orig']
        elif 'orig' not in self and 'rs2' not in self:
            self['rs1'][0] = self['rs1'][0] + self['rs1'].sum()
            return self['rs1']
        elif 'orig' not in self and 'rs1' in self and 'rs2' in self:
            self['rs1'][0] = self['rs1'][0] + self['rs2'].sum()
            return self['rs1']
        elif 'v0' in self:
            self['orig'][0] = self['rs1'][0] + np.ma.array(self['rs2'], mask=((self['v0'] + 1) & 0x1).astype(bool)).sum()
            return self['orig']
        else:
            self['orig'][0] = self['rs1'][0] + self['rs2'].sum()
            return self['orig']
