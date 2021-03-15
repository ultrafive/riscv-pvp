from isa.inst import *

class Veadd_mf(Inst):
  name = 'veadd.mf'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1']+self['rs2'].astype('float16')