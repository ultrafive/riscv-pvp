from isa.inst import *

class Vesub_mf(Inst):
  name = 'vesub.mf'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1']-self['rs2'].astype('float16')