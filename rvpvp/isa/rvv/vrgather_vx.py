from ...isa.inst import *
import numpy as np

class Vrgather_vi(Inst):
    name = 'vrgather.vi'
    # vrgather.vi vd, vs2, uimm, vm # vd[i] = (uimm >= VLMAX) ? 0 : vs2[uimm]
    def golden(self):
        vlmax = self.get_VLMAX(self['sew'],self['lmul'])
        vlValid  = min(vlmax, self['vl'])
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        result = self['ori'].copy()
       
        for ii in range (vstart, vlValid):
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['uimm'] >= vlmax:
                    result[ii] = 0
                else:
                    if self['uimm'] >= vlValid:
                        if 'tail' in self:
                            result[ii] = self['vs2'][self['uimm']]
                        else:
                            result[ii] = 0
                    else:
                        result[ii] = self['vs2'][self['uimm']]
        return result


class Vrgather_vx(Inst):
    name = 'vrgather.vx'
    # vrgather.vx vd, vs2, rs1, vm # vd[i] = (x[rs1] >= VLMAX) ? 0 : vs2[x[rs1]]
    def golden(self):
        vlmax = self.get_VLMAX(self['sew'],self['lmul'])
        vlValid  = min(vlmax, self['vl'])
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        result = self['ori'].copy()
       
        for ii in range (vstart, vlValid):
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['rs1'] >= vlmax:
                    result[ii] = 0
                else:
                    if self['rs1'] >= vlValid:
                        if 'tail' in self:
                            result[ii] = self['vs2'][self['rs1']]
                        else:
                            result[ii] = 0
                    else:
                        result[ii] = self['vs2'][self['rs1']]
        return result


class Vrgather_vv(Inst):
    name = 'vrgather.vv'
    # vrgather.vv vd, vs2, vs1, vm # vd[i] = (vs1[i] >= VLMAX) ? 0 : vs2[vs1[i]]; 
    def golden(self):
        vlmax = self.get_VLMAX(self['sew'],self['lmul'])
        vlValid  = min(vlmax, self['vl'])
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        result = self['ori'].copy()
       
        for ii in range (vstart, vlValid):
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] >= vlmax:
                    result[ii] = 0
                else:
                    if self['vs1'][ii] >= vlValid:
                        if 'tail' in self:
                            result[ii] = self['vs2'][self['vs1'][ii]]
                        else:
                            result[ii] = 0
                    else:
                        result[ii] = self['vs2'][self['vs1'][ii]]
        return result


class Vrgatherei16_vv(Inst):
    name = 'vrgatherei16.vv'
    # vrgatherei16.vv vd, vs2, vs1, vm # vd[i] = (vs1[i] >= VLMAX) ? 0 : vs2[vs1[i]];
    def golden(self):
        vlmax = self.get_VLMAX(self['sew'],self['lmul'])
        vlValid  = min(vlmax, self['vl'])
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        result = self['ori'].copy()
       
        for ii in range (vstart, vlValid):
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] >= vlmax:
                    result[ii] = 0
                else:
                    if self['vs1'][ii] >= vlValid:
                        if 'tail' in self:
                            result[ii] = self['vs2'][self['vs1'][ii]]
                        else:
                            result[ii] = 0
                    else:
                        result[ii] = self['vs2'][self['vs1'][ii]]
        return result

