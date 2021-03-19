from isa.inst import *
import numpy as np

class Vesqrt_m(Inst):
  name = 'vesqrt.m'

  def golden(self):
    if 'rs1' in self.keys():
      return np.sqrt(self['rs1'])