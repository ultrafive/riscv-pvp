from ...isa.inst import *
import numpy as np


class Vmfeq_vv(Inst):
    name = 'vmfeq.vv'

    def golden(self):
        if 'vs2' in self:

            result = np.unpackbits( self['orig'], bitorder='little' )


            if 'vstart' in self:
                vstart = self['vstart']
            else:
                vstart = 0

            if 'mask' in self:
                mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vl']]
            else:
                if self['vl'] >= vstart:
                    mask = np.ones( self['vl'] - vstart, dtype = np.uint8 )

            for no in range(vstart, self['vl']):
                if mask[ no - vstart ] == 1:
                    result[ no ] = self['vs1'][no] == self['vs2'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0


class Vmfne_vv(Inst):
    name = 'vmfne.vv'

    def golden(self):
        if 'vs2' in self:

            result = np.unpackbits( self['orig'], bitorder='little' )

            if 'vstart' in self:
                vstart = self['vstart']
            else:
                vstart = 0

            if 'mask' in self:
                mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vl']]
            else:
                if self['vl'] >= vstart:
                    mask = np.ones( self['vl'] - vstart, dtype = np.uint8 )

            for no in range(vstart, self['vl']):
                if mask[ no - vstart ] == 1:
                    result[ no ] = self['vs1'][no] != self['vs2'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0
    

class Vmflt_vv(Inst):
    name = 'vmflt.vv'

    def golden(self):
        if 'vs2' in self:
            
            result = np.unpackbits( self['orig'], bitorder='little' )

            if 'vstart' in self:
                vstart = self['vstart']
            else:
                vstart = 0

            if 'mask' in self:
                mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vl']]
            else:
                if self['vl'] >= vstart:
                    mask = np.ones( self['vl'] - vstart, dtype = np.uint8 )

            for no in range(vstart, self['vl']):
                if mask[ no - vstart ] == 1:
                    result[ no ] = self['vs2'][no] < self['vs1'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0
        

class Vmfle_vv(Inst):
    name = 'vmfle.vv'

    def golden(self):
        if 'vs2' in self:
            
            result = np.unpackbits( self['orig'], bitorder='little' )

            if 'vstart' in self:
                vstart = self['vstart']
            else:
                vstart = 0

            if 'mask' in self:
                mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vl']]
            else:
                if self['vl'] >= vstart:
                    mask = np.ones( self['vl'] - vstart, dtype = np.uint8 )

            for no in range(vstart, self['vl']):
                if mask[ no - vstart ] == 1:
                    result[ no ] = self['vs2'][no] <= self['vs1'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0
                                     
