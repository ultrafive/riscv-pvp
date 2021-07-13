from isa.inst import *
import numpy as np

class Vwredsumu_vs(Inst):
    name = 'vwredsumu.vs'
    def golden(self):
        maskflag = 1 if 'mask' in self else 0
        self['ori'][0] = self['vs1'][0]
        for ii in range(self['vl']):            
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                self['ori'][0] += self['vs2'][ii]
        return self['ori']

class Vwredsum_vs(Vwredsumu_vs):
    name = 'vwredsum.vs'


