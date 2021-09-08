from ...isa.inst import *
import numpy as np
import struct

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfadd_vf(Inst):
    name = 'vfadd.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['rs1'] + self['vs2'][vstart:self['vl']],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0        



class Vfsub_vf(Inst):
    name = 'vfsub.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] - self['rs1'],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         
        


class Vfrsub_vf(Inst):
    name = 'vfrsub.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['rs1'] - self['vs2'][vstart:self['vl']],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         

 

class Vfmul_vf(Inst):
    name = 'vfmul.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['rs1'] * self['vs2'][vstart:self['vl']],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         
     

class Vfdiv_vf(Inst):
    name = 'vfdiv.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] / self['rs1'] ,
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         
 

class Vfrdiv_vf(Inst):
    name = 'vfrdiv.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['rs1'] / self['vs2'][vstart:self['vl']],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         

def max( a, b ):
    result = np.zeros( b.size, dtype=b.dtype )
    for no in range(0, b.size):
        if np.isnan( a ):
            result[no] = b[no]
        elif np.isnan( b[no] ):
            result[no] = a
        else:
            result[no] = np.maximum( a, b[no] ) 

    return result   

class Vfmax_vf(Inst):
    name = 'vfmax.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( max( self['rs1'], self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0 

def min_vf( a, b ):
    result = np.zeros( b.size, dtype=b.dtype )
    for no in range(0, b.size):
        if np.isnan( a ):
            result[no] = b[no]
        elif np.isnan( b[no] ):
            result[no] = a
        else:
            result[no] = np.minimum( a, b[no] )      

    return result        
                    


class Vfmin_vf(Inst):
    name = 'vfmin.vf'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( min_vf( self['rs1'], self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0  

class Vfsgnj_vf(Inst):
    name = 'vfsgnj.vf'

    def golden(self):
        if 'vs2' in self:
            if self['vs2'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs2'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs2'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.where( struct.unpack( str_int, struct.pack( str_float, self['rs1'] ) )[0] >> signal_bit, - abs( self['vs2'][vstart:self['vl']] ), abs( self['vs2'][vstart:self['vl']] ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0


class Vfsgnjn_vf(Inst):
    name = 'vfsgnjn.vf'

    def golden(self):
        if 'vs2' in self:
            if self['vs2'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs2'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs2'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.where( struct.unpack( str_int, struct.pack( str_float, self['rs1'] ) )[0] >> signal_bit, abs( self['vs2'][vstart:self['vl']] ), - abs( self['vs2'][vstart:self['vl']] ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfsgnjx_vf(Inst):
    name = 'vfsgnjx.vf'

    def golden(self):
        if 'vs2' in self:
            if self['vs2'].dtype == np.float16:
                str_int = '<H'
                str_float = '<e'
                signal_bit = 15
            elif self['vs2'].dtype == np.float32:
                str_int = '<I'
                str_float = '<f'
                signal_bit = 31            

            elif self['vs2'].dtype == np.float64:
                str_int = '<Q'
                str_float = '<d'
                signal_bit = 63

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            vd = np.zeros( self['vl'] - vstart, dtype = self['vs2'].dtype )
            for i, v in enumerate(self['vs2'][vstart:self['vl']]):
                vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, self['rs1'] ) )[0] >> signal_bit  == 
                struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, abs( v ), - abs( v ) )

            result[vstart:self['vl']] = self.masked( vd, self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0                                