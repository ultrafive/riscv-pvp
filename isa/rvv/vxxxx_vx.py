from isa.inst import *
import numpy as np

class Vmacc_vx(Inst):
    name = 'vmacc.vx'

    def golden(self):
        return self.masked(self['vd'] + self['rs1'] * self['vs2'], self['vd'])

class Vnmsac_vx(Inst):
    name = 'vnmsac.vx'

    def golden(self):
        return self.masked(- (self['rs1'] * self['vs2']) + self['vd'], self['vd'])

class Vmadd_vx(Inst):
    name = 'vmadd.vx'

    def golden(self):
        return self.masked(self['rs1'] * self['vd'] + self['vs2'], self['vd'])

class Vnmsub_vx(Inst):
    name = 'vnmsub.vx'

    def golden(self):
        return self.masked(- (self['rs1'] * self['vd']) + self['vs2'], self['vd'])
