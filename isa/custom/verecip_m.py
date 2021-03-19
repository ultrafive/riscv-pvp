from isa.inst import *
import numpy as np

class Verecip_m(Inst):
  name = 'verecip.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.reciprocal(self['rs1'])