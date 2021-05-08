from isa.inst import *
import numpy as np

class Vfslide1up_vf(Inst):
    name = 'vfslide1up.vf'

    def golden(self):

        vd = self['vs2'].tolist()
        vd.insert( 0, self['rs1'].astype( self['vs2'].dtype ) )
        vd = np.array(vd[:-1], dtype=self['vs2'].dtype )
        return self.masked( vd, self['orig'] if 'orig' in self else 0 )


class Vfslide1down_vf(Inst):
    name = 'vfslide1down.vf'

    def golden(self):

        vd = self['vs2'].tolist()
        vd =vd[1:]
        vd.append( self['rs1'].astype( self['vs2'].dtype ) )
        vd = np.array(vd, dtype=self['vs2'].dtype )
        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

