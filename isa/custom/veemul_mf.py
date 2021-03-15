from isa.inst import *

class Veemul_mf(Inst):
  name = 'veemul.mf'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1'] * (self['rs2'].astype('float16'))