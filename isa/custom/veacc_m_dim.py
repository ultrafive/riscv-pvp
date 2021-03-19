from isa.inst import *
import numpy as np

class Veacc_m_dim(Inst):
  name = 'veacc.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.sum( self['rs1'], axis = self['dim'] )