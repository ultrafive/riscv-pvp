from isa.inst import *
import numpy as np
import math

class Vmadc_vi(Inst):
    name = 'vmadc.vi'

    def golden(self):
        vd = self['vs2'].astype(np.uint64) + self['imm']
        vd=np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmseq_vi(Inst):
    name = 'vmseq.vi'

    def golden(self):
        vd = self.masked(self['vs2'] == self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsne_vi(Inst):
    name = 'vmsne.vi'

    def golden(self):
        vd = self.masked(self['vs2'] != self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsleu_vi(Inst):
    name = 'vmsleu.vi'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsle_vi(Inst):
    name = 'vmsle.vi'

    def golden(self):
        vd = self.masked(self['vs2'] <= self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsgtu_vi(Inst):
    name = 'vmsgtu.vi'

    def golden(self):
        vd = self.masked(self['vs2'] > self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsgt_vi(Inst):
    name = 'vmsgt.vi'

    def golden(self):
        vd = self.masked(self['vs2'] > self['imm'])
        return np.packbits(vd, bitorder='little')[0: self['vl']]