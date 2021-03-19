from isa.inst import *
import numpy as np

class Veemul_x8_hf_mf(Inst):
  name = 'veemul.x8.hf.mf'

  def golden(self):
    if 'rs1' in self.keys():
      rd = self['rs1']*(self['rs2'].astype('float16'))
      return rd.astype(np.int8)