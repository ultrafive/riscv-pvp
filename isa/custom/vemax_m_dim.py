from isa.inst import *
import numpy as np

class Vemax_m_dim(Inst):
  name = 'vemax.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.amax( self['rs1'], axis = self['dim'] )