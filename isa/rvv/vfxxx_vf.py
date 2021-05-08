from isa.inst import *
import numpy as np
import struct

class Vfadd_vf(Inst):
    name = 'vfadd.vf'

    def golden(self):

        return self.masked( self['rs1'].astype( self['vs2'].dtype ) + self['vs2'], self['orig'] if 'orig' in self else 0 )


class Vfsub_vf(Inst):
    name = 'vfsub.vf'

    def golden(self):
        return self.masked( self['vs2'] - self['rs1'].astype( self['vs2'].dtype ), self['orig'] if 'orig' in self else 0 )


class Vfrsub_vf(Inst):
    name = 'vfrsub.vf'

    def golden(self):
        return self.masked( self['rs1'].astype( self['vs2'].dtype ) - self['vs2'], self['orig'] if 'orig' in self else 0 )
 

class Vfmul_vf(Inst):
    name = 'vfmul.vf'

    def golden(self):
        return self.masked( self['rs1'].astype( self['vs2'].dtype ) * self['vs2'], self['orig'] if 'orig' in self else 0 )
     

class Vfdiv_vf(Inst):
    name = 'vfdiv.vf'

    def golden(self):
        return self.masked( self['vs2'] / self['rs1'].astype( self['vs2'].dtype ) , self['orig'] if 'orig' in self else 0 )
 

class Vfrdiv_vf(Inst):
    name = 'vfrdiv.vf'

    def golden(self):
        return self.masked( self['rs1'].astype( self['vs2'].dtype ) /self['vs2'], self['orig'] if 'orig' in self else 0 )


class Vfmax_vf(Inst):
    name = 'vfmax.vf'

    def golden(self):
        vd = np.zeros( self['vs2'].size, dtype=self['vs2'].dtype )
        for no in range(0, self['vs2'].size):
            if np.isnan( self['rs1'].astype( self['vs2'].dtype ) ):
                vd[no] = self['vs2'][no]
            elif np.isnan( self['vs2'][no] ):
                vd[no] = self['rs1'].astype( self['vs2'].dtype )
            else:
                vd[no] = np.maximum( self['rs1'].astype( self['vs2'].dtype ), self['vs2'][no] )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 ) 


class Vfmin_vf(Inst):
    name = 'vfmin.vf'

    def golden(self):
        vd = np.zeros( self['vs2'].size, dtype=self['vs2'].dtype )
        for no in range(0, self['vs2'].size):
            if np.isnan( self['rs1'].astype( self['vs2'].dtype ) ):
                vd[no] = self['vs2'][no]
            elif np.isnan( self['vs2'][no] ):
                vd[no] = self['rs1'].astype( self['vs2'].dtype )
            else:
                vd[no] = np.minimum( self['rs1'].astype( self['vs2'].dtype ), self['vs2'][no] )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )    


class Vfsgnj_vf(Inst):
    name = 'vfsgnj.vf'

    def golden(self):
        
        vd = np.where( struct.unpack( '<I', struct.pack( '<f', self['rs1'] ) )[0] >> 31, -abs( self['vs2'] ), abs( self['vs2'] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )   


class Vfsgnjn_vf(Inst):
    name = 'vfsgnjn.vf'

    def golden(self):
        
        vd = np.where( struct.unpack( '<I', struct.pack( '<f', self['rs1'] ) )[0] >> 31, abs( self['vs2'] ), -abs( self['vs2'] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 ) 

class Vfsgnjx_vf(Inst):
    name = 'vfsgnjx.vf'

    def golden(self):
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs2']):
            vd[i] = np.where( struct.unpack( '<I', struct.pack( '<f', self['rs1'] ) )[0] >> 31 == 
            struct.unpack( '<I', struct.pack( '<f', self['vs2'][i] ) )[0] >> 31, abs( self['vs2'][i] ), -abs( self['vs2'][i] ) )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )                                   