from isa.inst import *
import numpy as np

class Vfmacc_vv(Inst):
    name = 'vfmacc.vv'

    def golden(self):
        return self.masked( self['vs1'] * self['vs2'] + self['vd'], self['vd'] )


class Vfnmacc_vv(Inst):
    name = 'vfnmacc.vv'

    def golden(self):
        return self.masked( - self['vs1'] * self['vs2'] - self['vd'], self['vd'] )


class Vfmsac_vv(Inst):
    name = 'vfmsac.vv'

    def golden(self):
        return self.masked( self['vs1'] * self['vs2'] - self['vd'], self['vd'] )


class Vfnmsac_vv(Inst):
    name = 'vfnmsac.vv'

    def golden(self):
        return self.masked( - self['vs1'] * self['vs2'] + self['vd'], self['vd'] ) 

class Vfmadd_vv(Inst):
    name = 'vfmadd.vv'

    def golden(self):
        return self.masked( self['vd'] * self['vs1'] + self['vs2'], self['vd'] )

class Vfnmadd_vv(Inst):
    name = 'vfnmadd.vv'

    def golden(self):
        return self.masked( - self['vd'] * self['vs1'] - self['vs2'], self['vd'] )


class Vfmsub_vv(Inst):
    name = 'vfmsub.vv'

    def golden(self):
        return self.masked( self['vd'] * self['vs1'] - self['vs2'], self['vd'] )
 

class Vfnmsub_vv(Inst):
    name = 'vfnmsub.vv'

    def golden(self):
        return self.masked( - self['vd'] * self['vs1'] + self['vs2'], self['vd'] )

