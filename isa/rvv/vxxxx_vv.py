from isa.inst import *
import numpy as np

class Vmacc_vv(Inst):
    name = 'vmacc.vv'

    def golden(self):
        return self.masked(self['vd'] + self['vs1'] * self['vs2'], self['vd'])

class Vnmsac_vv(Inst):
    name = 'vnmsac.vv'

    def golden(self):
        return self.masked(- (self['vs1'] * self['vs2']) + self['vd'], self['vd'])

class Vmadd_vv(Inst):
    name = 'vmadd.vv'

    def golden(self):
        return self.masked(self['vs1'] * self['vd'] + self['vs2'], self['vd'])

class Vnmsub_vv(Inst):
    name = 'vnmsub.vv'

    def golden(self):
        return self.masked(- (self['vs1'] * self['vd']) + self['vs2'], self['vd'])
