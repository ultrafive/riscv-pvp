from isa.inst import *
import numpy as np

class Vzext_vf2(Inst):
    name = 'vzext.vf2'

    def golden(self):
        return self.masked(self['vs2'].astype(np.uint16))

class Vzext_vf4(Inst):
    name = 'vzext.vf4'

    def golden(self):
        return self.masked(self['vs2'].astype(np.uint32))

class Vzext_vf8(Inst):
    name = 'vzext.vf8'

    def golden(self):
        return self.masked(self['vs2'].astype(np.uint64))

class Vsext_vf2(Inst):
    name = 'vsext.vf2'

    def golden(self):
        return self.masked(self['vs2'].astype(np.int16))

class Vsext_vf4(Inst):
    name = 'vsext.vf4'

    def golden(self):
        return self.masked(self['vs2'].astype(np.int32))

class Vsext_vf8(Inst):
    name = 'vsext.vf8'

    def golden(self):
        return self.masked(self['vs2'].astype(np.int64))