from isa.inst import *
import numpy as np
import math

class Vmsof_m(Inst):
    name = 'vmsof.m'

    def golden(self):
        if 'mask' in self:
            tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vlen']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vlen']]
        res = np.zeros(self['vlen'], dtype=np.uint8)
        if np.size(np.where(tmp == 1)) > 0:
          firstOne = np.min(np.where(tmp == 1))
          res[firstOne] = 1
        return np.packbits(res, bitorder='little')


class Vmsbf_m(Inst):
    name = 'vmsbf.m'

    def golden(self):
        if 'mask' in self:
            tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vlen']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vlen']]
        res = np.ones(self['vlen'], dtype=np.uint8)
        if np.size(np.where(tmp == 1)) > 0:
          firstOne = np.min(np.where(tmp == 1))
          for i in range(firstOne, self['vlen']):
            res[i] = 0
        if 'mask' in self:
          mask = np.unpackbits(self['mask'], bitorder='little')[0:self['vlen']]
          res = np.where( mask == 1, res, 0)
        return np.packbits(res, bitorder='little')

class Vmsif_m(Inst):
    name = 'vmsif.m'

    def golden(self):
        if 'mask' in self:
            tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vlen']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vlen']]
        res = np.ones(self['vlen'], dtype=np.uint8)
        if np.size(np.where(tmp == 1)) > 0:
          firstOne = np.min(np.where(tmp == 1))
          for i in range(firstOne+1, self['vlen']):
            res[i] = 0
        if 'mask' in self:
          mask = np.unpackbits(self['mask'], bitorder='little')[0:self['vlen']]
          res = np.where( mask == 1, res, 0)
        return np.packbits(res, bitorder='little')
