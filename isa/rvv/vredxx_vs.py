from isa.inst import *
import numpy as np

class Vredsum_vs(Inst):
    name = 'vredsum.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.sum(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd

class Vredmaxu_vs(Inst):
    name = 'vredmaxu.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.amax(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd

class Vredmax_vs(Vredmaxu_vs):
    name = 'vredmax.vs'

class Vredminu_vs(Inst):
    name = 'vredminu.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.amin(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd

class Vredmin_vs(Vredminu_vs):
    name = 'vredmin.vs'

class Vredand_vs(Inst):
    name = 'vredand.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.bitwise_and.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd

class Vredor_vs(Inst):
    name = 'vredor.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.bitwise_or.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd

class Vredxor_vs(Inst):
    name = 'vredxor.vs'

    def golden(self):
        vd = self['orig'].copy()
        vd[0] = np.bitwise_xor.reduce(self['vs2'], where=self.where(), initial=self['vs1'][0])

        return vd