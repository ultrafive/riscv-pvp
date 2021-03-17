from isa.inst import *
import numpy as np

class Vemin_m_dim(Inst):
  name = 'vemin.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.amin( self['rs1'], axis = self['dim'] )