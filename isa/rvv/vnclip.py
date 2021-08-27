from isa.inst import *
import numpy as np

class Vnclip_wv(Inst):
    name = 'vnclip.wv'
    # vnclip.wv vd, vs2, vs1, vm 
    # vd[i] = clip(roundoff_signed(vs2[i], vs1[i]))   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        
        if self['vs2'].dtype == self['vs1'].dtype: 
            self['vs1'].dtype = self.get_intdtype(self['sew'])  

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        int_max = np.iinfo(self.get_intdtype(self['sew'])).max
        int_min = np.iinfo(self.get_intdtype(self['sew'])).min
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['vs1'][ii] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > int_max:
                    result[ii] = int_max
                    #print('exit saturation up  : vs1 = '+str(self['vs1'][ii])+ '  vs2 = '+str(self['vs2'][ii]))   
                elif tmp[0] < int_min:
                    result[ii] = int_min
                    #print('exit saturation down: vs1 = '+str(self['vs1'][ii])+ '  vs2 = '+str(self['vs2'][ii]))    
                else:
                    result[ii] = tmp[0]     
        return result     


class Vnclipu_wv(Inst):
    name = 'vnclipu.wv'
    # vnclipu.wv vd, vs2, vs1, vm  
    # vd[i] = clip(roundoff_unsigned(vs2[i], vs1[i]))
    def golden(self):
        if self['vl']==0:
            return self['ori']
        
        if self['vs2'].dtype == self['vs1'].dtype: 
            self['vs1'].dtype = self.get_uintdtype(self['sew'])  

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        uint_max = np.iinfo(self.get_uintdtype(self['sew'])).max
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['vs1'][ii] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > uint_max:
                    result[ii] = uint_max
                    #print('exit saturation : vs1 = '+str(self['vs1'][ii])+ '  vs2 = '+str(self['vs2'][ii]))   
                else:
                    result[ii] = tmp[0]     
        return result 


class Vnclip_wx(Inst):
    name = 'vnclip.wx'
    # vnclip.wx vd, vs2, rs1, vm
    # vd[i] = clip(roundoff_signed(vs2[i], x[rs1]))  
    def golden(self):
        if self['vl']==0:
            return self['ori']
 
        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        int_max = np.iinfo(self.get_intdtype(self['sew'])).max
        int_min = np.iinfo(self.get_intdtype(self['sew'])).min
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['rs1'] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > int_max:
                    result[ii] = int_max
                    #print('exit saturation up  : rs1 = '+str(self['rs1'])+ '  vs2 = '+str(self['vs2'][ii]))   
                elif tmp[0] < int_min:
                    result[ii] = int_min
                    #print('exit saturation down: rs1 = '+str(self['rs1'])+ '  vs2 = '+str(self['vs2'][ii]))    
                else:
                    result[ii] = tmp[0]     
        return result     


class Vnclipu_wx(Inst):
    name = 'vnclipu.wx'
    # vnclipu.wx vd, vs2, rs1, vm  
    # vd[i] = clip(roundoff_unsigned(vs2[i], x[rs1]))   
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        uint_max = np.iinfo(self.get_uintdtype(self['sew'])).max
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['rs1'] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > uint_max:
                    result[ii] = uint_max
                    #print('exit saturation : rs1 = '+str(self['rs1'])+ '  vs2 = '+str(self['vs2'][ii]))   
                else:
                    result[ii] = tmp[0]     
        return result     



class Vnclip_wi(Inst):
    name = 'vnclip.wi'
    # vnclip.wi vd, vs2, uimm, vm  
    # vd[i] = clip(roundoff_signed(vs2[i], uimm)) 
    def golden(self):
        if self['vl']==0:
            return self['ori']
 
        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        int_max = np.iinfo(self.get_intdtype(self['sew'])).max
        int_min = np.iinfo(self.get_intdtype(self['sew'])).min
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['uimm'] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > int_max:
                    result[ii] = int_max
                    #print('exit saturation up  : uimm = '+str(self['uimm'])+ '  vs2 = '+str(self['vs2'][ii]))   
                elif tmp[0] < int_min:
                    result[ii] = int_min
                    #print('exit saturation down: uimm = '+str(self['uimm'])+ '  vs2 = '+str(self['vs2'][ii]))    
                else:
                    result[ii] = tmp[0]     
        return result     
    

class Vnclipu_wi(Inst):
    name = 'vnclipu.wi'
    # vnclipu.wi vd, vs2, uimm, vm  
    # vd[i] = clip(roundoff_unsigned(vs2[i], uimm))  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        uint_max = np.iinfo(self.get_uintdtype(self['sew'])).max
        tmp = np.array([0], dtype='object') 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['uimm'] % self['sew2']
                tmp[0] = self.rounding_xrm( self['vs2'][ii], vxrm, shift ) 
                if  tmp[0] > uint_max:
                    result[ii] = uint_max
                    #print('exit saturation : uimm = '+str(self['uimm'])+ '  vs2 = '+str(self['vs2'][ii]))   
                else:
                    result[ii] = tmp[0]     
        return result      
   
