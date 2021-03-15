from isa.inst import *
import numpy as np

class Veemul_x32_mf(Inst):
  name = 'veemul.x32.mf'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1'].astype('float16') * (self['rs2'].astype('float16'))