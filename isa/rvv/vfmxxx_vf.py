from isa.inst import *
import numpy as np

class Vfmacc_vf(Inst):
    name = 'vfmacc.vf'

    def golden(self):
        return self.masked( self['vs2'] * self['rs1'].astype(self['vs2'].dtype) + self['vd'], self['vd'] )

class Vfnmacc_vf(Inst):
    name = 'vfnmacc.vf'

    def golden(self):
        return self.masked( - self['vs2'] * self['rs1'].astype(self['vs2'].dtype) - self['vd'], self['vd'] )

class Vfmsac_vf(Inst):
    name = 'vfmsac.vf'

    def golden(self):
        return self.masked( self['vs2'] * self['rs1'].astype(self['vs2'].dtype) - self['vd'], self['vd'] )

class Vfnmsac_vf(Inst):
    name = 'vfnmsac.vf'

    def golden(self):
        return self.masked( - self['vs2'] * self['rs1'].astype(self['vs2'].dtype) + self['vd'], self['vd'] )          


class Vfmadd_vf(Inst):
    name = 'vfmadd.vf'

    def golden(self):
        return self.masked( self['vd'] * self['rs1'].astype(self['vs2'].dtype) + self['vs2'], self['vd'] )

class Vfnmadd_vf(Inst):
    name = 'vfnmadd.vf'

    def golden(self):
        return self.masked( - self['vd'] * self['rs1'].astype(self['vs2'].dtype) - self['vs2'], self['vd'] )

class Vfmsub_vf(Inst):
    name = 'vfmsub.vf'

    def golden(self):
        return self.masked( self['vd'] * self['rs1'].astype(self['vs2'].dtype) - self['vs2'], self['vd'] )

class Vfnmsub_vf(Inst):
    name = 'vfnmsub.vf'

    def golden(self):
        return self.masked( - self['vd'] * self['rs1'].astype(self['vs2'].dtype) + self['vs2'], self['vd'] )

