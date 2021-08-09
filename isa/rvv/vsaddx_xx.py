from isa.inst import *
import math


class Vsadd_vv(Inst):
    name = 'vsadd.vv'
    def golden(self):
        res = np.add(self['vs1'], self['vs2'], dtype='object')[0: self['vl']]
        res = self.masked(res)
        res = np.where(res > np.iinfo(self['vs1'].dtype).max, np.iinfo(self['vs1'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs1'].dtype).min, np.iinfo(self['vs1'].dtype).min, res)
        return res.astype(self['vs1'].dtype)

class Vsadd_vx(Inst):
    name = 'vsadd.vx'
    def golden(self):
        res = self['rs1'] + self['vs2'].astype('object')
        res = self.masked(res[0: self['vl']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)

class Vsadd_vi(Inst):
    name = 'vsadd.vi'
    def golden(self):
        res = self['imm'] + self['vs2'].astype('object')
        res = self.masked(res[0: self['vl']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)

class Vsaddu_vv(Inst):
    name = 'vsaddu.vv'
    def golden(self):
        res = np.add(self['vs1'], self['vs2'], dtype='object')[0: self['vl']]
        res = self.masked(res)
        res = np.where(res > np.iinfo(self['vs1'].dtype).max, np.iinfo(self['vs1'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs1'].dtype).min, np.iinfo(self['vs1'].dtype).min, res)
        return res.astype(self['vs1'].dtype)

class Vsaddu_vx(Inst):
    name = 'vsaddu.vx'
    def golden(self):
        res = self['rs1'] + self['vs2'].astype('object')
        res = self.masked(res[0: self['vl']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)

class Vsaddu_vi(Inst):
    name = 'vsaddu.vi'
    def golden(self):
        res = self['imm'] + self['vs2'].astype('object')
        res = self.masked(res[0: self['vl']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)