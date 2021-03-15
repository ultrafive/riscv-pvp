from isa.inst import *

class Veadd_mv(Inst):
  name = 'veadd.mv'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1']+self['vs2']