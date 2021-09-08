from ...isa.inst import *
import numpy as np

class Vcompress_vm(Inst):
    name = 'vcompress.vm'
    ''' Example use of vcompress instruction:
        1 1 0 1 0 0 1 0 1 v0  
        8 7 6 5 4 3 2 1 0 v1  
        1 2 3 4 5 6 7 8 9 v2  
                                vcompress.vm v2, v1, v0  
        1 2 3 4 8 7 5 2 0 v2
    '''
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()        
        index  = 0
        for ii in range (self['vl']): 
            if np.unpackbits(self['mask'], bitorder='little')[ii]:
                result[index] = self['vs2'][ii] 
                index += 1   
        return result
