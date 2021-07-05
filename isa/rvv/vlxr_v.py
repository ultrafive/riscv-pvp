from isa.inst import *
import math

class _Vlxr_v(Inst):
    def golden(self):
        return self['rs1']
    


class Vlxre8_v(_Vlxr_v):
    name = 'vlxre8.v'

class Vlxre16_v(_Vlxr_v):
    name = 'vlxre16.v'    

class Vlxre32_v(_Vlxr_v):
    name = 'vlxre32.v'

class Vlxre64_v(_Vlxr_v):
    name = 'vlxre64.v'    

