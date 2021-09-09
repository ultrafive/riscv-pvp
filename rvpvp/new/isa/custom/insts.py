from rvpvp.isa.inst import *

# class Vmod_vv(Inst):
#     '''Sample instruction implement
#         vmod.vv vd, vs2, vs1, vm
#         vd[i] = vs1[i] % vs2[i]
#     '''
#     name = 'vmod.vv'
 
#     def golden(self):
#         if 'vs1' in self:
#             if 'orig' in self:
#                 result = self['orig'].copy()
#             else:
#                 result = np.zeros( self['vl'], dtype = self['vs1'].dtype )

#             vstart = self['vstart'] if 'vstart' in self else 0

#             result[vstart:self['vl']] = self.masked(
#                 self['vs1'][vstart:self['vl']] % self['vs2'][vstart:self['vl']],
#                 self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

#             return result
#         else:
#             return 0