from isa.inst import *
import numpy as np
import math

class Vmadc_vx(Inst):
    name = 'vmadc.vx'

    def golden(self):
        vd = self['vs2'].astype(np.int64) + self['rs1']
        vd = np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsbc_vx(Inst):
    name = 'vmsbc.vx'

    def golden(self):
        vd = self['vs2'].astype(np.int64) - self['rs1']
        vd = np.where(vd < 0, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmseq_vx(Inst):
    name = 'vmseq.vx'

    def golden(self):
        vd = self.masked(self['vs2'] == self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsne_vx(Inst):
    name = 'vmsne.vx'

    def golden(self):
        vd = self.masked(self['vs2'] != self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsltu_vx(Inst):
    name = 'vmsltu.vx'

    def golden(self):
        vd = self.masked(self['vs2'] < self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmslt_vx(Inst):
    name = 'vmslt.vx'

    def golden(self):
        vd = self.masked(self['vs2'] < self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsleu_vx(Inst):
    name = 'vmsleu.vx'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]


class Vmsle_vx(Inst):
    name = 'vmsle.vx'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsgtu_vx(Inst):
    name = 'vmsgtu.vx'

    def golden(self):
        vd = self.masked(self['vs2'] > self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]


class Vmsgt_vx(Inst):
    name = 'vmsgt.vx'

    def golden(self):
        vd = self.masked(self['vs2'] > self['rs1'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]
