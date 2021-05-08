from isa.inst import *
import numpy as np

class Vmfeq_vv(Inst):
    name = 'vmfeq.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs1'] == self['vs2'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )


class Vmfne_vv(Inst):
    name = 'vmfne.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs1'] != self['vs2'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )
    

class Vmflt_vv(Inst):
    name = 'vmflt.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] < self['vs1'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )
        

class Vmfle_vv(Inst):
    name = 'vmfle.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] <= self['vs1'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )

class Vmfgt_vv(Inst):
    name = 'vmfgt.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] > self['vs1'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )
         

class Vmfge_vv(Inst):
    name = 'vmfge.vv'

    def golden(self):
        if 'orig' in self:
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            orig = np.array(orig).astype(np.bool_)

        return self.masked( ( self['vs2'] >= self['vs1'] ).astype( np.bool_ ), orig if 'orig' in self else 0 )
                                     
