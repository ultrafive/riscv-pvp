from isa.inst import *
import numpy as np

class Vfwadd_wf(Inst):
    name = 'vfwadd.wf'

    def golden(self):
        return self.masked( self['rs1'].astype( self['vs2'].dtype ) + self['vs2'], self['orig'] if 'orig' in self else 0 )


class Vfwsub_wf(Inst):
    name = 'vfwsub.wf'

    def golden(self):
        return self.masked( self['vs2'] - self['rs1'].astype( self['vs2'].dtype ), self['orig'] if 'orig' in self else 0 )

