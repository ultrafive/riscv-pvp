from isa.inst import *

class Vesub_mv(Inst):
  name = 'vesub.mv'

  def golden(self):
    if 'rs1' in self.keys():
      return self['rs1']-self['vs2']