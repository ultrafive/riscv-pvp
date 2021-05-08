from isa.inst import *
import numpy as np
import math

class Vlexff_v(Inst):
    name = 'vlexff.v'

    def golden(self):

        vd = self['rs1'].copy()

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )


class Vle8ff_v(Vlexff_v):
    name = 'vle8ff.v'


class Vle16ff_v(Vlexff_v):
    name = 'vle16ff.v'


class Vle32ff_v(Vlexff_v):
    name = 'vle32ff.v'


class Vle64ff_v(Vlexff_v):
    name = 'vle64ff.v'

                       