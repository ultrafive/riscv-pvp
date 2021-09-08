from ...isa.inst import *
import numpy as np
import struct
import numpy as np

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfadd_vv(Inst):
    name = 'vfadd.vv'

    def golden(self):

        if 'vs1' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] + 
            self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0
        
class Vfsub_vv(Inst):
    name = 'vfsub.vv'

    def golden(self):

        if 'vs1' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] - 
            self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0        

class Vfmul_vv(Inst):
    name = 'vfmul.vv'

    def golden(self):

        if 'vs1' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] * 
            self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 
                                         
                libm.fesetround( 0 )        

            return result
        else:
            return 0        


class Vfdiv_vv(Inst):
    name = 'vfdiv.vv'

    def golden(self):

        if 'vs1' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] /
            self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

def max(a, b, size):
    result = np.maximum( a, b )
    for i in range( size ):
        if np.isnan( a[i] ):
            result[i] = b[i]
        else:
            if np.isnan( b[i] ):
                result[ i ] = a[i]
    return result  

class Vfmax_vv(Inst):
    name = 'vfmax.vv'

    def golden(self):

        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( max(self['vs2'][vstart:self['vl']], 
            self['vs1'][vstart:self['vl']], self['vl'] - vstart ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0        
    
def min_vv(a, b, size):
    result = np.minimum( a, b )
    for i in range( size ):
        if np.isnan( a[i] ):
            result[i] = b[i]
        else:
            if np.isnan( b[i] ):
                result[ i ] = a[i]
    return result    


class Vfmin_vv(Inst):
    name = 'vfmin.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( min_vv(self['vs2'][vstart:self['vl']], 
            self['vs1'][vstart:self['vl']], self['vl'] - vstart ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0



class Vfsgnj_vv(Inst):
    name = 'vfsgnj.vv'

    def golden(self):
        if 'vs1' in self:
            if self['vs1'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs1'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs1'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.zeros( self['vl'] - vstart, dtype = self['vs2'].dtype )
            for i, v in enumerate(self['vs1'][vstart:self['vl']]):
                vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, -abs( self['vs2'][i + vstart] ), abs( self['vs2'][i+vstart] ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0



class Vfsgnjn_vv(Inst):
    name = 'vfsgnjn.vv'

    def golden(self):
        if 'vs1' in self:
            if self['vs1'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs1'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs1'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.zeros( self['vl'] - vstart, dtype = self['vs2'].dtype )
            for i, v in enumerate(self['vs1'][vstart:self['vl']]):
                vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, abs( self['vs2'][i + vstart] ), -abs( self['vs2'][i+vstart] ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfsgnjx_vv(Inst):
    name = 'vfsgnjx.vv'

    def golden(self):
        if 'vs1' in self:
            if self['vs1'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs1'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs1'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.zeros( self['vl'] - vstart, dtype = self['vs2'].dtype )
            for i, v in enumerate(self['vs1'][vstart:self['vl']]):
                vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit == 
                struct.unpack( str_int, struct.pack( str_float, self['vs2'][i + vstart] ) )[0] >> signal_bit, abs( self['vs2'][i + vstart] ), -abs( self['vs2'][i + vstart] ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0
