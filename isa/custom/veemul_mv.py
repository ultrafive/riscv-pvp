from isa.inst import *

class Veemul_mv(Inst):
  name = 'veemul.mv'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1']*self['vs2']