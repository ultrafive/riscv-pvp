from isa.inst import *
import numpy as np
import math

class Vmadc_vv(Inst):
    name = 'vmadc.vv'

    def golden(self):
        vd = self['vs2'].astype(np.uint64) + self['vs1']
        vd=np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsbc_vv(Inst):
    name = 'vmsbc.vv'

    def golden(self):
        vd = self['vs2'].astype(np.int64) - self['vs1']
        vd=np.where(vd < 0, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmseq_vv(Inst):
    name = 'vmseq.vv'

    def golden(self):
        vd = self.masked(self['vs2'] == self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsne_vv(Inst):
    name = 'vmsne.vv'

    def golden(self):
        vd = self.masked(self['vs2'] != self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsltu_vv(Inst):
    name = 'vmsltu.vv'

    def golden(self):
        vd = self.masked(self['vs2'] < self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmslt_vv(Inst):
    name = 'vmslt.vv'

    def golden(self):
        vd = self.masked(self['vs2'] < self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsleu_vv(Inst):
    name = 'vmsleu.vv'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsle_vv(Inst):
    name = 'vmsle.vv'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['vs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]