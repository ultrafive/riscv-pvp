from isa.inst import *
import math

class _Vlxr_v(Inst):
    def golden(self):
        return self['rs1']

class Vl1r_v(_Vlxr_v):
    name = 'vl1r.v'

class Vl1re8_v(_Vlxr_v):
    name = 'vl1re8.v'

class Vl1re16_v(_Vlxr_v):
    name = 'vl1re16.v'    

class Vl1re32_v(_Vlxr_v):
    name = 'vl1re32.v'

class Vl1re64_v(_Vlxr_v):
    name = 'vl1re64.v'    

class Vl2r_v(_Vlxr_v):
    name = 'vl2r.v'

class Vl2re8_v(_Vlxr_v):
    name = 'vl2re8.v'

class Vl2re16_v(_Vlxr_v):
    name = 'vl2re16.v'    

class Vl2re32_v(_Vlxr_v):
    name = 'vl2re32.v'

class Vl2re64_v(_Vlxr_v):
    name = 'vl2re64.v'    

class Vl4r_v(_Vlxr_v):
    name = 'vl4r.v'

class Vl4re8_v(_Vlxr_v):
    name = 'vl4re8.v'

class Vl4re16_v(_Vlxr_v):
    name = 'vl4re16.v'    

class Vl4re32_v(_Vlxr_v):
    name = 'vl4re32.v'

class Vl4re64_v(_Vlxr_v):
    name = 'vl4re64.v'    

class Vl8r_v(_Vlxr_v):
    name = 'vl8r.v'

class Vl8re8_v(_Vlxr_v):
    name = 'vl8re8.v'

class Vl8re16_v(_Vlxr_v):
    name = 'vl8re16.v'    

class Vl8re32_v(_Vlxr_v):
    name = 'vl8re32.v'

class Vl8re64_v(_Vlxr_v):
    name = 'vl8re64.v'            