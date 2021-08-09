from isa.inst import *
import numpy as np
import struct

class Vfadd_vv(Inst):
    name = 'vfadd.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] + self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0
        
class Vfsub_vv(Inst):
    name = 'vfsub.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] - self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfmul_vv(Inst):
    name = 'vfmul.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] * self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            if 'frm' in self and self['frm'] == 1:
                for i in range(len(result)):
                    if np.isposinf( result[i] ):
                        result[i] = 65504
                    elif np.isneginf( result[i] ):
                        result[i] = -65504

            return result

        else:
            return 0


class Vfdiv_vv(Inst):
    name = 'vfdiv.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'][vstart:self['vl']] / self['vs1'][vstart:self['vl']], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0


class Vfmax_vv(Inst):
    name = 'vfmax.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( np.maximum(self['vs2'][vstart:self['vl']], self['vs1'][vstart:self['vl']]), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0        
    

class Vfmin_vv(Inst):
    name = 'vfmin.vv'

    def golden(self):
        if 'vs1' in self:
            if 'orig' in self:
                result = self['orig'].copy()
                if 'mask' in self or 'vstart' in self:
                    result = result[0:self['vl']]
            else:
                result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( np.minimum(self['vs2'][vstart:self['vl']], self['vs1'][vstart:self['vl']]), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0



class Vfsgnj_vv(Inst):
    name = 'vfsgnj.vv'

    def golden(self):
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
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs1']):
            vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, -abs( self['vs2'][i] ), abs( self['vs2'][i] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )



class Vfsgnjn_vv(Inst):
    name = 'vfsgnjn.vv'

    def golden(self):
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
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs1']):
            vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, abs( self['vs2'][i] ), -abs( self['vs2'][i] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfsgnjx_vv(Inst):
    name = 'vfsgnjx.vv'

    def golden(self):
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
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs1']):
            vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit == 
            struct.unpack( str_int, struct.pack( str_float, self['vs2'][i] ) )[0] >> signal_bit, abs( self['vs2'][i] ), -abs( self['vs2'][i] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )
