from ...isa.inst import *
import numpy as np

class Vmfeq_vf(Inst):
    name = 'vmfeq.vf'

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
                    result[ no ] = self['rs1'] == self['vs2'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0


class Vmfne_vf(Inst):
    name = 'vmfne.vf'

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
                    result[ no ] = self['rs1'] != self['vs2'][no]
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0

class Vmflt_vf(Inst):
    name = 'vmflt.vf'

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
                    result[ no ] =  self['vs2'][no] < self['rs1']
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0


class Vmfle_vf(Inst):
    name = 'vmfle.vf'

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
                    result[ no ] =  self['vs2'][no] <= self['rs1']
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0



class Vmfgt_vf(Inst):
    name = 'vmfgt.vf'

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
                    result[ no ] =  self['vs2'][no] > self['rs1']
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0
 

class Vmfge_vf(Inst):
    name = 'vmfge.vf'

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
                    result[ no ] =  self['vs2'][no] >= self['rs1']
            
            result = np.packbits( result, bitorder='little' )

            return result

        else:
            return 0


