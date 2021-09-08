from ...isa.inst import *
import numpy as np

class Vsadd_vv(Inst):
    name = 'vsadd.vv'
    # vsadd.vv vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']

        ori = self['ori'].copy()       
        tmp = np.add(self['vs2'], self['vs1'], dtype='object')#[0: self['vl']]
        result = self.masked(tmp, ori)

        vstart = self['vstart'] if 'vstart' in self else 0
        if vstart:
            for ii in range(min(vstart, self['vl'])):
                result[ii] = ori[ii]
        if 'tail' in self:
            for ii in range(self['vl'], self['tail']):
                result[ii] = ori[ii]

        result = np.where(result > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, result)
        result = np.where(result < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, result)
        return result.astype(self['vs2'].dtype)

class Vsaddu_vv(Vsadd_vv):
    name = 'vsaddu.vv'


class Vsadd_vx(Inst):
    name = 'vsadd.vx'
    # vsadd.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        ori = self['ori'].copy()       
        tmp = np.add(self['vs2'], self['rs1'], dtype='object')#[0: self['vl']]
        result = self.masked(tmp, ori)

        vstart = self['vstart'] if 'vstart' in self else 0
        if vstart:
            for ii in range(min(vstart, self['vl'])):
                result[ii] = ori[ii]
        if 'tail' in self:
            for ii in range(self['vl'], self['tail']):
                result[ii] = ori[ii]

        result = np.where(result > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, result)
        result = np.where(result < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, result)
        return result.astype(self['vs2'].dtype)    

class Vsaddu_vx(Vsadd_vx):
    name = 'vsaddu.vx'


class Vsadd_vi(Inst):
    name = 'vsadd.vi'
    # vsadd.vi vd, vs2, imm, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        ori = self['ori'].copy()       
        tmp = np.add(self['vs2'], self['imm'], dtype='object')#[0: self['vl']]
        result = self.masked(tmp, ori)

        vstart = self['vstart'] if 'vstart' in self else 0
        if vstart:
            for ii in range(min(vstart, self['vl'])):
                result[ii] = ori[ii]
        if 'tail' in self:
            for ii in range(self['vl'], self['tail']):
                result[ii] = ori[ii]

        result = np.where(result > np.iinfo(self['vs2'].dtype).max, np.iinfo(self['vs2'].dtype).max, result)
        result = np.where(result < np.iinfo(self['vs2'].dtype).min, np.iinfo(self['vs2'].dtype).min, result)
        return result.astype(self['vs2'].dtype)   


class Vsaddu_vi(Vsadd_vi):
    name = 'vsaddu.vi'
          