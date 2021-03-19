from isa.inst import *
import numpy as np

class Veemul_x32_mv(Inst):
  name = 'veemul.x32.mv'

  def golden(self):
    if 'rs1' in self.keys():
      rs1 = self['rs1'].astype(np.int32)
      return rs1.astype(np.float16) * self['vs2']