from isa.inst import *
import math

class Vsxr_v(Inst):
    def golden(self):
        return self['rs1']

class Vsxre8_v(Vsxr_v):
    name = 'vsxre8.v'

class Vsxre16_v(Vsxr_v):
    name = 'vsxre16.v'

class Vsxre32_v(Vsxr_v):
    name = 'vsxre32.v'

class Vsxre64_v(Vsxr_v):
    name = 'vsxre64.v'    

  
          