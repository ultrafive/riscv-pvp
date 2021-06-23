from isa.inst import *
import math


class Vaadd_vv(Inst):
    name = 'vaadd.vv'
    def golden(self):
        res = np.add(self['vs1'], self['vs2'], dtype='int')[0: self['vlen']]
        res = self.masked(res)
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs1'].dtype)

class Vaadd_vx(Inst):
    name = 'vaadd.vx'
    def golden(self):
        res = self['rs1'] + self['vs2'].astype('int')
        res = self.masked(res[0: self['vlen']])
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs2'].dtype)

class Vasub_vv(Inst):
    name = 'vasub.vv'
    def golden(self):
        res = np.subtract(self['vs2'], self['vs1'], dtype='int')[0: self['vlen']]
        res = self.masked(res)
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs1'].dtype)

class Vasub_vx(Inst):
    name = 'vasub.vx'
    def golden(self):
        res = self['vs2'].astype('int') - self['rs1']
        res = self.masked(res[0: self['vlen']])
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs2'].dtype)

class Vaaddu_vv(Inst):
    name = 'vaaddu.vv'
    def golden(self):
        res = np.add(self['vs1'], self['vs2'], dtype='uint')[0: self['vlen']]
        res = self.masked(res)
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs1'].dtype)

class Vaaddu_vx(Inst):
    name = 'vaaddu.vx'
    def golden(self):
        res = self['rs1'] + self['vs2'].astype('uint')
        res = self.masked(res[0: self['vlen']])
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs2'].dtype)

class Vasubu_vv(Inst):
    name = 'vasubu.vv'
    def golden(self):
        res = np.subtract(self['vs2'], self['vs1'], dtype='long')[0: self['vlen']]
        res = self.masked(res)
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs1'].dtype)

class Vasubu_vx(Inst):
    name = 'vasubu.vx'
    def golden(self):
        res = self['vs2'].astype('long') - self['rs1']
        res = self.masked(res[0: self['vlen']])
        res = self.rounding(res)
        return np.right_shift(res, 1).astype(self['vs2'].dtype)