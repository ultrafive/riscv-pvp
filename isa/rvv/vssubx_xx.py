from isa.inst import *
import math

class Vssub_vv(Inst):
    name = 'vssub.vv'
    def golden(self):
        res = np.subtract(self['vs2'], self['vs1'], dtype='object')[0: self['vlen']]
        res = self.masked(res)
        res = np.where(res > np.iinfo(self['vs1'].dtype).max, np.iinfo(self['vs1'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs1'].dtype).min, np.iinfo(self['vs1'].dtype).min, res)
        return res.astype(self['vs1'].dtype)

class Vssub_vx(Inst):
    name = 'vssub.vx'
    def golden(self):
        res = self['vs2'].astype('object') -self['rs1']
        res = self.masked(res[0: self['vlen']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)

class Vssubu_vv(Inst):
    name = 'vssubu.vv'
    def golden(self):
        res = np.subtract(self['vs2'], self['vs1'], dtype='object')[0: self['vlen']]
        res = self.masked(res)
        res = np.where(res > np.iinfo(self['vs1'].dtype).max, np.iinfo(self['vs1'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs1'].dtype).min, np.iinfo(self['vs1'].dtype).min, res)
        return res.astype(self['vs1'].dtype)

class Vssubu_vx(Inst):
    name = 'vssubu.vx'
    def golden(self):
        res = self['vs2'].astype('object') -self['rs1']
        res = self.masked(res[0: self['vlen']])
        res = np.where(res > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, res)
        res = np.where(res < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, res)
        return res.astype(self['vs2'].dtype)