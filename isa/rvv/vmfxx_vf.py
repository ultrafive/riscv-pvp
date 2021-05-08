from isa.inst import *
import numpy as np

class Vmfeq_vf(Inst):
    name = 'vmfeq.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( np.array(self['rs1']).astype(self['vs2'].dtype) == self['vs2'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )


class Vmfne_vf(Inst):
    name = 'vmfne.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( np.array(self['rs1']).astype(self['vs2'].dtype) != self['vs2'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )

class Vmflt_vf(Inst):
    name = 'vmflt.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] < np.array(self['rs1']).astype(self['vs2'].dtype) ).astype( np.bool_ ), orig if 'orig' in self else 0 )


class Vmfle_vf(Inst):
    name = 'vmfle.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] <= np.array(self['rs1']).astype(self['vs2'].dtype) ).astype( np.bool_ ), orig if 'orig' in self else 0 )



class Vmfgt_vf(Inst):
    name = 'vmfgt.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] > np.array(self['rs1']).astype(self['vs2'].dtype) ).astype( np.bool_ ), orig if 'orig' in self else 0 )
 

class Vmfge_vf(Inst):
    name = 'vmfge.vf'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs2'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] >= np.array(self['rs1']).astype(self['vs2'].dtype) ).astype( np.bool_ ), orig if 'orig' in self else 0 )


