from isa.inst import *
import numpy as np

class Vse8_v(Inst):
    name = 'vse8.v'

    def golden(self):
        if 'mask' not in self:
            return self['rs1']
        else:
            mask_list = []
            if 'vlen' in self:
                v0_mask = self['mask']
                for index in range(0, self['vlen']):
                    if v0_mask & 1 == 0:
                        mask_list.append(True)
                    else:
                        mask_list.append(False)

                    v0_mask = v0_mask >> 1

            return np.ma.array(self['rs1'], mask = mask_list, fill_value = 0).filled()
