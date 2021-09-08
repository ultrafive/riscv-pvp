from ...isa.inst import *
import math

class Vssub_vv(Inst):
    name = 'vssub.vv'
    # vssub.vv vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']

        ori = self['ori'].copy()       
        tmp = np.subtract(self['vs2'], self['vs1'], dtype='object')
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
 
class Vssubu_vv(Vssub_vv):
    name = 'vssubu.vv'


class Vssub_vx(Inst):
    name = 'vssub.vx'
    # vssub.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        ori = self['ori'].copy()       
        tmp = np.subtract(self['vs2'], self['rs1'], dtype='object')
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


class Vssubu_vx(Vssub_vx):
    name = 'vssubu.vx'
