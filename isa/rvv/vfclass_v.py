from isa.inst import *
import numpy as np

def f16_classify( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype = np.uint16 )

    for no in range( vs2.size ):
        num = int( np.array( [vs2[no]], dtype = np.float16 ).byteswap().tobytes().hex(), 16 )
        
        infOrNaN = ( ( num >> 10 ) & 0x1F ) == 0x1F
        subnormalOrZero = ( ( num >> 10 ) & 0x1F ) == 0
        sign = num >> 15
        fracZero = ( num & 0x3FF ) == 0
        isNaN = infOrNaN and ( not fracZero )
        isSNaN =  ( ( num & 0x7E00 ) == 0x7C00 ) and ( num & 0x1FF )
        vd[no] = ( 
        (  sign and infOrNaN and fracZero ) << 0 | 
        (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
        (  sign and subnormalOrZero and not fracZero )  << 2 |
        (  sign and subnormalOrZero and fracZero )   << 3 |
        ( not sign and subnormalOrZero and fracZero )   << 4 | 
        ( not sign and subnormalOrZero and not fracZero )  << 5 |
        ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
        ( not sign and infOrNaN and fracZero )          << 7 |
        ( isNaN and  isSNaN )                       << 8 |
        ( isNaN and not isSNaN )                       << 9  )

    return vd

def f32_classify( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype = np.uint32 )

    for no in range( vs2.size ):
        num = int( np.array( [vs2[no]], dtype = np.float32 ).byteswap().tobytes().hex(), 16 )
        
        infOrNaN = ( ( num >> 23 ) & 0xFF ) == 0xFF
        subnormalOrZero = ( ( num >> 23 ) & 0xFF ) == 0
        sign = num >> 31
        fracZero = ( num & 0x7FFFFF ) == 0
        isNaN = infOrNaN and ( not fracZero )
        isSNaN =  ( ( num & 0x7FC00000 ) == 0x7F800000 ) and ( num & 0x3FFFFF )
        vd[no] = ( 
        (  sign and infOrNaN and fracZero ) << 0 | 
        (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
        (  sign and subnormalOrZero and not fracZero )  << 2 |
        (  sign and subnormalOrZero and fracZero )   << 3 |
        ( not sign and subnormalOrZero and fracZero )   << 4 | 
        ( not sign and subnormalOrZero and not fracZero )  << 5 |
        ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
        ( not sign and infOrNaN and fracZero )          << 7 |
        ( isNaN and  isSNaN )                       << 8 |
        ( isNaN and not isSNaN )                       << 9  )

    return vd

def f64_classify( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype = np.uint64 )

    for no in range( vs2.size ):
        num = int( np.array( [vs2[no]], dtype = np.float64 ).byteswap().tobytes().hex(), 16 )
        
        infOrNaN = ( ( num >> 52 ) & 0x7FF ) == 0x7FF
        subnormalOrZero = ( ( num >> 52 ) & 0x7FF ) == 0
        sign = num >> 63
        fracZero = ( num & 0xFFFFFFFFFFFFF ) == 0
        isNaN = infOrNaN and ( not fracZero )
        isSNaN =  ( ( num & 0x7FF8000000000000 ) == 0x7FF0000000000000 ) and ( num & 0x7FFFFFFFFFFFF )
        vd[no] = ( 
        (  sign and infOrNaN and fracZero ) << 0 | 
        (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
        (  sign and subnormalOrZero and not fracZero )  << 2 |
        (  sign and subnormalOrZero and fracZero )   << 3 |
        ( not sign and subnormalOrZero and fracZero )   << 4 | 
        ( not sign and subnormalOrZero and not fracZero )  << 5 |
        ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
        ( not sign and infOrNaN and fracZero )          << 7 |
        ( isNaN and  isSNaN )                       << 8 |
        ( isNaN and not isSNaN )                       << 9  )

    return vd


class Vfclass_v(Inst):
    name = 'vfclass.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            vd = f16_classify( self['vs2'] )
        elif self['vs2'].dtype == np.float32:
            vd = f32_classify( self['vs2'] )
        elif self['vs2'].dtype == np.float64:
            vd = f64_classify( self['vs2'] )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )
