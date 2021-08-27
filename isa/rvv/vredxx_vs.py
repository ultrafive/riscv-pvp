from isa.inst import *
import numpy as np

class Vredsum_vs(Inst):
    name = 'vredsum.vs'
    # vd[0] = sum( vs1[0] , vs2[*] )
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] += self['vs2'][ii]
        return result


class Vredmax_vs(Inst):
    name = 'vredmax.vs'
    # vd[0] = maxu( vs1[0] , vs2[*] )
    # self['ori'][0] = np.amax(self['vs2'], where=self.where(), initial=self['vs1'][0])
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] = max(self['vs2'][ii], result[0])
        return result

class Vredmaxu_vs(Vredmax_vs):
    name = 'vredmaxu.vs'
    # vd[0] = maxu( vs1[0] , vs2[*] )


class Vredmin_vs(Inst):
    name = 'vredmin.vs'
    # vd[0] = min( vs1[0] , vs2[*] )
    # vd[0] = np.amin(self['vs2'], where=self.where(), initial=self['vs1'][0])
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] = min(self['vs2'][ii], result[0])
        return result

class Vredminu_vs(Vredmin_vs):
    name = 'vredminu.vs'


class Vredand_vs(Inst):
    name = 'vredand.vs'
    # vd[0] = and( vs1[0] , vs2[*] )
    # self['ori'][0] = np.bitwise_and.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] = self['vs2'][ii] & result[0]
        return result    


class Vredor_vs(Inst):
    name = 'vredor.vs'
    # vd[0] = or( vs1[0] , vs2[*] )
    # self['ori'][0] = np.bitwise_or.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] = self['vs2'][ii] | result[0]
        return result  


class Vredxor_vs(Inst):
    name = 'vredxor.vs'
    # vd[0] = xor( vs1[0] , vs2[*] )
    # self['ori'][0] = np.bitwise_xor.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        result[0] = self['vs1'][0]
        for ii in range(self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[0] = self['vs2'][ii] ^ result[0]
        return result
        
        