from isa.inst import *
import numpy as np

class Veacc_m(Inst):
  name = 'veacc.m'

  def golden(self):
    if 'rs1' in self.keys():
      rd = np.sum(self['rs1'])
      return np.array(rd).astype(np.float32)