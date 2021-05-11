from isa.inst import *
import math

class Vsxr_v(Inst):
    def golden(self):
        return self['vs']

class Vs1r_v(Vsxr_v):
    name = 'vs1r.v'

class Vs2r_v(Vsxr_v):
    name = 'vs2r.v'

class Vs4r_v(Vsxr_v):
    name = 'vs4r.v'

class Vs8r_v(Vsxr_v):
    name = 'vs8r.v'    

  
          