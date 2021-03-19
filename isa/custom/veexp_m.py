from isa.inst import *
import numpy as np

class Veexp_m(Inst):
  name = 'veexp.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.exp(self['rs1'])