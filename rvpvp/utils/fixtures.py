'''You can use functions and lists in this module to generate data for cases.
'''

import numpy as np

from .params import ( 
    factor_lmul, 
    double_lmul_dict, 
    string_lmul, 
    fldins_dict, 
    fstins_dict, 
    get_uintdtype
)


def random_mask( vl ):
    '''Function used to generate random mask bits for rvv instructions.

    Args:
        vl (int): vl register value, which defines mask bits amount in this function.
    
    Returns:
        numpy ndarray: A random numpy ndarray, its dtype is numpy.uint8, its size is the integer which is rounded up to after vl is divided by 8.
        The bits above vl are 0.
    '''
    mask =  np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int16)), dtype=np.uint8)
    mask = np.unpackbits( mask, bitorder='little' )[0:vl]
    mask = np.packbits( mask, bitorder='little' )
    return mask

def zero_mask( vl ):
    '''Function used to generate zero mask bits for rvv instruction.

    Args:
        vl (int): vl register value, which defines mask bits amount in this function.

    Returns:
        numpy ndarray: A zero numpy ndarray, its dtype is numpy.uint8, its size is the integer which is rounded up to after vl is divided by 8.
    '''
    mask =  np.zeros( int(np.ceil(vl/8)), dtype=np.uint8 )
    return mask 

def mask_first( vl ):
    '''Function used to generate mask bits of which the first bit is 0, others are 1 for rvv instruction.

    Args:
        vl (int): vl register value, which defines mask bits amount in this function.

    Returns:
        numpy ndarray: A numpy ndarray of which the first bit of first element is 0, others are 1, its dtype is numpy.uint8, its size is the integer which is rounded up to after vl is divided by 8.
    '''
    mask =  np.ones( vl, dtype=np.uint8 )
    mask[0] = 0
    mask = np.packbits( mask, bitorder='little' )
    return mask 

def mask_last( vl ):
    '''Function used to generate mask bits of which the vlth bit is 0, others are 1 for rvv instruction.

    Args:
        vl (int): vl register value, which defines mask bits amount in this function.

    Returns:
        numpy ndarray: A numpy ndarray of which the vlth bit is 0, others are 1, its dtype is numpy.uint8, its size is the integer which is rounded up to after vl is divided by 8.
    '''  
    mask =  np.ones( vl, dtype=np.uint8 )
    mask[vl-1] = 0
    mask = np.packbits( mask, bitorder='little' )
    return mask

def special_fp16():
    '''Function to generate a list of special float16 numbers.

    Returns:
        list: A list of 8 numpy ndarrays of which size is 1 and dtype is numpy.float16.
        There is a special float16 number in every numpy ndarray.
        The special numbers are 0, inf, nan, 0.1, 10, 65500, 6.104e-5, 6e-8.
    '''
    # 0   ,  inf  ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    fpt0 = np.array([0x0000], dtype=np.int16)
    fpt1 = np.array([0x7c00], dtype=np.int16)
    fpt2 = np.array([0x7e00], dtype=np.int16)
    fpt3 = np.array([0x2e66], dtype=np.int16)
    fpt4 = np.array([0x4900], dtype=np.int16)
    fpt5 = np.array([0x7bff], dtype=np.int16)
    fpt6 = np.array([0x0400], dtype=np.int16)
    fpt7 = np.array([0x0001], dtype=np.int16)   

    fpt = [ fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7 ]
    for fpt_data in fpt:
        fpt_data.dtype = np.float16

    return fpt  

def special_fp32():
    '''Function to generate a list of special float32 numbers.

    Returns:
        list: A list of 8 numpy ndarrays of which size is 1 and dtype is numpy.float32.
        There is a special float32 number in every numpy ndarray.
        The special numbers are 0, inf, nan, 0.1, 10, 3.40282e+38, 1.1755e-38, 1e-45.
    '''    
    # 0   ,       inf  ,       nan  ,      0.1  ,      10  , 3.40282e+38,  1.1755e-38,      1e-45
    fpt0 = np.array([0x00000000], dtype=np.int32)
    fpt1 = np.array([0x7f800000], dtype=np.int32)
    fpt2 = np.array([0x7fc00000], dtype=np.int32)
    fpt3 = np.array([0x3dcccccd], dtype=np.int32)
    fpt4 = np.array([0x41200000], dtype=np.int32)
    fpt5 = np.array([0x7f7fffff], dtype=np.int32)
    fpt6 = np.array([0x00800000], dtype=np.int32)
    fpt7 = np.array([0x00000001], dtype=np.int32)

    fpt = [ fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7 ]
    for fpt_data in fpt:
        fpt_data.dtype = np.float32

    return fpt 

def special_fp64():
    '''Function to generate a list of special float64 numbers.

    Returns:
        list: A list of 8 numpy ndarrays of which size is 1 and dtype is numpy.float64.
        There is a special float64 number in every numpy ndarray.
        The special numbers are 0, inf, nan, 0.1, 10, 1.79769313e+308, 2.22507386e-308, 5.e-324.
    '''     
    #0   ,               inf  ,               nan  ,              0.1  ,               10  ,    1.79769313e+308,     2.22507386e-308,         5.e-324
    fpt0 = np.array([0x0000000000000000], dtype=np.uint64)
    fpt1 = np.array([0x7ff0000000000000], dtype=np.uint64)
    fpt2 = np.array([0x7ff8000000000000], dtype=np.uint64)
    fpt3 = np.array([0x3fb999999999999a], dtype=np.uint64)
    fpt4 = np.array([0x4024000000000000], dtype=np.uint64)
    fpt5 = np.array([0x7fefffffffffffff], dtype=np.uint64)
    fpt6 = np.array([0x0010000000000000], dtype=np.uint64)
    fpt7 = np.array([0x0000000000000001], dtype=np.uint64)     

    fpt = [ fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7 ]
    for fpt_data in fpt:
        fpt_data.dtype = np.float64

    return fpt 

def special_float(sew):
    '''Function to generate a list special float numbers of which the data type is depended on sew.

    Args:
        sew (int):  sew decides the element width and data type for special float numbers.
            16 - float16
            32 - float32
            64 - float64

    Returns:
        list: A list of 8 numpy ndarrays. 
        When sew == 16, return the result of special_fp16().
        When sew == 32, return the result of special_fp32().
        When sew == 64, return the result of special_fp64().
    '''
    if sew == 16:
        return special_fp16()
    if sew == 32:
        return special_fp32()
    if sew == 64:
        return special_fp64()   

def special_vv_fp16():
    '''Function to generate a list of 2 numpy ndarrays which include 32 special float16 numbers.

    Returns:
        list: The list includes 2 numpy ndarrays. There are 32 special float16 numbers in every ndarray.
        The corresponding elements pairs in these ndarrays are different and comprehensive. So users 
        can use these two ndarrays to test the results between two special float16 numbers.
    '''
    # special float table          -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    fpt0 = np.array([[0x0000]*6, [0x8000, 0x7c00,         0x7e00,                 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt1 = np.array([[0x7c00]*8, [        0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt2 = np.array([[0x7e00]*6, [                        0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt3 = np.array([[0x2e66]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt4 = np.array([[0x4900]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt5 = np.array([[0x7bff]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt6 = np.array([[0x0400]*2, [                                                        0x0400, 0x0001]], dtype=np.int16)
    fpt7 = np.array([[0x0001]*1, [                                                                0x0001]], dtype=np.int16)   

    fpt_data = np.concatenate((fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7), axis=1)
    fpt_data.dtype = np.float16

    return [ fpt_data[0], fpt_data[1] ] 

def special_vv_fp32():
    '''Function to generate a list of 2 numpy ndarrays which include 32 special float32 numbers.

    Returns:
        list: The list includes 2 numpy ndarrays. There are 32 special float32 numbers in every ndarray.
        The corresponding elements pairs in these ndarrays are different and comprehensive. So users 
        can use these two ndarrays to test the results between two special float32 numbers.
    '''    
    # special float table                  -0   ,       inf  ,       -inf ,       nan  ,      0.1  ,      10  , 3.40282e+38,  1.1755e-38,      1e-45
    fpt0 = np.array([[0x00000000]*6, [0x80000000,  0x7f800000,               0x7fc00000,                         0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt1 = np.array([[0x7f800000]*8, [             0x7f800000,  0xff800000,  0x7fc00000, 0x3dcccccd, 0x41200000, 0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt2 = np.array([[0x7fc00000]*6, [                                       0x7fc00000, 0x3dcccccd, 0x41200000, 0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt3 = np.array([[0x3dcccccd]*3, [                                                                           0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt4 = np.array([[0x41200000]*3, [                                                                           0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt5 = np.array([[0x7f7fffff]*3, [                                                                           0x7f7fffff,  0x00800000, 0x00000001]], dtype=np.int32)
    fpt6 = np.array([[0x00800000]*2, [                                                                                        0x00800000, 0x00000001]], dtype=np.int32)
    fpt7 = np.array([[0x00000001]*1, [                                                                                                    0x00000001]], dtype=np.int32)   

    fpt_data = np.concatenate((fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7), axis=1)
    fpt_data.dtype = np.float32

    return [ fpt_data[0], fpt_data[1] ]     

def special_vv_fp64():
    '''Function to generate a list of 2 numpy ndarrays which include 32 special float64 numbers.

    Returns:
        list: The list includes 2 numpy ndarrays. There are 32 special float64 numbers in every ndarray.
        The corresponding elements pairs in these ndarrays are different and comprehensive. So users 
        can use these two ndarrays to test the results between two special float64 numbers.
    '''      
    # special float table                                  -0   ,               inf  ,               -inf ,               nan  ,              0.1  ,               10  ,    1.79769313e+308,     2.22507386e-308,         5.e-324
    fpt0 = np.array([[0x0000000000000000]*6, [0x8000000000000000,  0x7ff0000000000000,                       0x7ff8000000000000,                                         0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt1 = np.array([[0x7ff0000000000000]*8, [                     0x7ff0000000000000,  0xfff0000000000000,  0x7ff8000000000000, 0x3fb999999999999a, 0x4024000000000000, 0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt2 = np.array([[0x7ff8000000000000]*6, [                                                               0x7ff8000000000000, 0x3fb999999999999a, 0x4024000000000000, 0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt3 = np.array([[0x3fb999999999999a]*3, [                                                                                                                           0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt4 = np.array([[0x4024000000000000]*3, [                                                                                                                           0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt5 = np.array([[0x7fefffffffffffff]*3, [                                                                                                                           0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt6 = np.array([[0x0010000000000000]*2, [                                                                                                                                                0x0010000000000000, 0x0000000000000001]], dtype=np.uint64)
    fpt7 = np.array([[0x0000000000000001]*1, [                                                                                                                                                                    0x0000000000000001]], dtype=np.uint64)   

    fpt_data = np.concatenate((fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7), axis=1)
    fpt_data.dtype = np.float64

    return [ fpt_data[0], fpt_data[1] ] 


def special_v_fp16():
    '''Function to generate a numpy ndarray which including 10 special float16 number.

    Returns:
        numpy ndarray: A float16 numpy ndarray, including [ 0, -0, inf, -inf, nan, 0.1, 10, 65500, 6.104e-05, 6.e-08 ]
    '''
    # special float table          -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    fpt_data = np.array([ 0x0000, 0x8000, 0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001], dtype=np.int16) 

    fpt_data.dtype = np.float16

    return fpt_data

def special_v_fp32():
    '''Function to generate a numpy ndarray which including 10 special float32 number.

    Returns:
        numpy ndarray: A float32 numpy ndarray, including [ 0, -0, inf, -inf, nan, 0.1, 10, 3.40282e+38, 1.1755e-38, 1e-45 ]
    '''    
    # special float table                  -0   ,       inf  ,       -inf ,       nan  ,      0.1  ,      10  , 3.40282e+38,  1.1755e-38,      1e-45
    fpt_data = np.array([ 0x00000000, 0x80000000,  0x7f800000,  0xff800000,  0x7fc00000, 0x3dcccccd, 0x41200000, 0x7f7fffff,  0x00800000, 0x00000001], dtype=np.int32)
 
    fpt_data.dtype = np.float32

    return fpt_data

def special_v_fp64():
    '''Function to generate a numpy ndarray which including 10 special float64 number.

    Returns:
        numpy ndarray: A float64 numpy ndarray, including [ 0, -0, inf, -inf, nan, 0.1, 10, 1.79769313e+308, 2.22507386e-308, 5.e-324 ]
    '''     
    # special float table                                  -0   ,               inf  ,               -inf ,               nan  ,              0.1  ,               10  ,    1.79769313e+308,     2.22507386e-308,         5.e-324
    fpt_data = np.array([ 0x0000000000000000, 0x8000000000000000,  0x7ff0000000000000,  0xfff0000000000000,  0x7ff8000000000000, 0x3fb999999999999a, 0x4024000000000000, 0x7fefffffffffffff,  0x0010000000000000, 0x0000000000000001], dtype=np.uint64)   

    fpt_data.dtype = np.float64

    return fpt_data

def special_v_float(sew):
    '''Function to generate a special float numpy ndarray of which the data type is decided by sew.
    
    Args:
        sew (int): sew decides the element width and data type for special float numbers.
            16 - float16
            32 - float32
            64 - float64

    Returns:
        numpy ndarray: When sew == 16, return the result of special_v_fp16().
        When sew == 32, return the result of special_v_fp32().
        When sew == 64, return the result of special_v_fp64().
    '''
    if sew == 16:
        return special_v_fp16()
    if sew == 32:
        return special_v_fp32()
    if sew == 64:
        return special_v_fp64() 

def get_sew_neq_eew(eew):
    '''Function to get available vsew values which don't equal to eew.

    Args:
        eew (int): The present eew value, which can be 8, 16, 32, 64.
    
    Returns:
        list: A list of available vsew values which don't equal to eew.
        The available vsew values are 8, 16, 32, 64.
    '''
    if 8 == eew:
        return [16, 32, 64]
    elif 16 == eew:
        return [8, 32, 64]
    elif 32 == eew:
        return [8, 16, 64]
    elif 64 == eew:
        return [8, 16, 32]

def get_lmul(sew_t):
    '''Function to get available lmul according to sew or sew and eew.

    Args:
        sew_t (int, tuple, list): If the type of sew_t is int, it is used as sew and eew.
            If the type of sew_t is tuple or list, the first element is used as sew, and 
            second element is used as eew.

    Returns:
        list: The list includes avaliable lmul value when sew and eew are set by sew_t.
    '''
    if type(sew_t) == int:
        sew = sew_t
        eew = sew
    elif type(sew_t) == tuple or type(sew_t) == list:
        sew = sew_t[0]
        eew = sew_t[1]
    if 8 == sew:
        tmp = [1,2,4,8,'f2','f4','f8']
    if 16 == sew:
        tmp = [1,2,4,8,'f2','f4']
    if 32 == sew:
        tmp = [1,2,4,8,'f2']
    if 64 == sew:
        tmp = [1,2,4,8]
    
    lmul_list = []
    for i in tmp:
        if (eew/sew*factor_lmul[i]) <= 8 and (eew/factor_lmul[i]) <= 64:
            lmul_list.append(i)
    
    return lmul_list

def get_seg_lmul(eew, sew, nf):
    '''Function to get avaliable lmul for segment instructions.

    Args:
        eew (int): Effective element width.
        sew (int): Selected element width.
        nf (int): nf field of segment instructions.

    Returns:
        list: The list includes avaliable lmul value with input eew, sew and nf for segment instructions.
    '''
    if 8 == sew:
        tmp = [1,2,4,8,'f2','f4','f8']
    if 16 == sew:
        tmp = [1,2,4,8,'f2','f4']
    if 32 == sew:
        tmp = [1,2,4,8,'f2']
    if 64 == sew:
        tmp = [1,2,4,8]

    lmul_list = []
    for i in tmp:
        if (eew/sew*factor_lmul[i]) <= 8 and (eew/factor_lmul[i]) <= 64 and (nf*eew/sew*factor_lmul[i]) <= 8:
            lmul_list.append(i)

    return lmul_list
    


def get_segi_lmul(eew, sew, nf):
    '''Function to get avaliable lmul for segment index instructions.

    Args:
        eew (int): Effective element width.
        sew (int): Selected element width.
        nf (int): nf field of segment instructions.

    Returns:
        list: The list includes avaliable lmul value with input eew, sew and nf for segment index instructions.
    '''    
    if 8 == sew:
        tmp = [1,2,4,8,'f2','f4','f8']
    if 16 == sew:
        tmp = [1,2,4,8,'f2','f4']
    if 32 == sew:
        tmp = [1,2,4,8,'f2']
    if 64 == sew:
        tmp = [1,2,4,8]

    lmul_list = []
    for i in tmp:
        if (eew/sew*factor_lmul[i]) <= 8 and (eew/factor_lmul[i]) <= 64 and (nf*factor_lmul[i]) <= 8:
            lmul_list.append(i)

    return lmul_list

def get_illegal_lmul(sew):
    '''Function to get illegal lmul with input sew.
    
    Args:
        sew (int): vsew register value, which can be 8, 16, 32, 64.

    Returns:
        list: illegal lmul with input sew, when sew == 8, return None.
    '''
    if 8 == sew:
        return None
    if 16 == sew:
        return ['f8']
    if 32 == sew:
        return ['f4', 'f8']
    if 64 == sew:
        return ['f2', 'f4', 'f8']    

def get_illegal_lmul_w(sew):
    '''Function to get illegal lmul values with input sew for widening and narrowing instructions.
    
    Args:
        sew (int): vsew register value, which can be 8, 16, 32, 64.

    Returns:
        list: illegal lmul with input sew for widening and narrowing instructions.
    '''    
    if 8 == sew:
        return [ 8 ]
    if 16 == sew:
        return ['f8', 8 ]
    if 32 == sew:
        return ['f4', 'f8', 8 ]
    if 64 == sew:
        return ['f2', 'f4', 'f8', 8 ]         

def get_lmul_w(sew):
    '''Function to get available lmul with input sew for widening and narrowing instructions.

    Args:
        sew (int): vsew register value, which can be 8, 16, 32, 64.

    Returns:
        list: The list includes avaliable lmul value with input sew for widening and narrowing instructions.
    '''    
    if 8 == sew:
        return [1,2,4,'f2','f4','f8']
    if 16 == sew:
        return [1,2,4,'f2','f4']
    if 32 == sew:
        return [1,2,4,'f2']
    if 64 == sew:
        return [1,2,4] 

def double_lmul(lmul):
    '''Function to compute double lmul value of input lmul.

    Args:
        lmul (int or str): lmul register value, which can be 1, 2, 4, '1', '2', '4', 'f2', 'f4', 'f8'

    Returns:
        int or str: double lmul value
    '''
    return double_lmul_dict[lmul]

def get_emul(eew, sew, lmul):
    '''Function to get emul based on sew, eew and lmul.

    Args:
        eew (int): effective element width 
        sew (int): selected element width
        lmul (int or str): vlmul register value

    Returns:
        int or str: computed emul value based eew/sew = emul/lmul

    '''
    return string_lmul[ (eew/sew)*factor_lmul[lmul] ]

def get_vl(lmul, ebits, vlen):
    '''Functions to get vl value based on vlen, sew, lmul

    Args:
        lmul (int or str): vlmul register value
        ebits (int): element bits length, which equals to vsew value.
        vlen (int): rvv register length

    Returns:
        list: A list including 1, vlmax, vlmax-1 and a value between 1 and vlmax-1.
        If  two values are equal, keep one value in the list.
    '''
    max = int( vlen * factor_lmul[lmul] / ebits )
    if 1 < max:
        if 1 < max-1:
            if 2 < max-1:
                mid = np.random.randint(2,max-1)
                return [1, mid, max-1, max]
            else:
                return [1, max-1, max]
        else:
            return [1, max]
    else:
        return [1]    

def get_vlmax(lmul, ebits, vlen):
    '''Function to get vlmax based on vlen, sew, lmul.
    
    Args:
        lmul (int or str): vlmul register value
        ebits (int): element bits length, which equals to vsew value.
        vlen (int): rvv register length
    
    Returns:
        int: vlmax value computed based on vlen*lmul/sew
    '''
    max = int( vlen * factor_lmul[lmul] / ebits )
    return max

def get_tailmax(lmul, ebits, vlen=1024):
    '''Function to get tail part maximum length in element units of vector operand.

    Args:
        lmul (int or str): vlmul register value
        ebits (int): element bits length, which equals to vsew value.
        vlen (int): rvv register length  

    Returns:
        int: tail part maximum length in element units. When lmul >= 1, it equals to vlmax.
        When lmul < 1, it equals to vlen/sew.
    '''    
    tail = max( vlen*factor_lmul[lmul]//ebits, vlen//ebits )
    return tail

def get_ls_vl(lmul, sew, eew, vlen):
    '''Function to get vl list for rvv load-store instruction

    Args:
        lmul (int or str): vlmul register value
        sew (int): vsew register value
        eew (int): effective element width set by load-store instruction
        vlen (int): rvv register length

    Returns:
        list: A list including test vl values for load-store instruction.
    '''
    emul = sew/eew * factor_lmul[lmul]
    emul = int( emul if emul >= 1 else 1)
    sum = int( vlen * factor_lmul[lmul] / sew )
    esum = int ( vlen * emul / eew)
    mid = np.random.randint(2,sum-1)
    if sum <= esum :
        return [1, mid, sum-1, sum]
    else:
        esum = int( vlen * factor_lmul[lmul] / eew )
        vl_list = [1]
        for i in range(1, emul+1):
            isum = int (vlen * i / eew)
            vl_list.append(isum - 1)
            vl_list.append(isum)
        return vl_list

def get_seg_vl(lmul, sew, eew, vlen):
    '''Function to get vl list for rvv segment load-store instruction

    Args:
        lmul (int or str): vlmul register value
        sew (int): vsew register value
        eew (int): effective element width set by load-store instruction
        vlen (int): rvv register length

    Returns:
        list: A list including test vl values for segment load-store instruction.
    '''    
    emul = sew/eew * factor_lmul[lmul]
    sum = int( vlen * factor_lmul[lmul] / sew )
    esum = int ( vlen * emul / eew)
    mid = np.random.randint(2,sum-1)
    if sum <= esum :
        return [1, mid, sum-1, sum]
    else:
        esum = int( vlen * factor_lmul[lmul] / eew )
        vl_list = [1]
        if emul < 1 :
            return [1, esum-1, esum]
        else:
            for i in range(1, int(emul+1)):
                isum = int (vlen * i / eew)
                vl_list.append(isum - 1)
                vl_list.append(isum)
        return vl_list

def get_random_vl(lmul, sew, eew, vlen):
    '''Functions to get random vl list based on lmul, sew, eew, vlen.

    Args:
        lmul (int or str): vlmul register value
        sew (int): vsew register value
        eew (int): effective element width
        vlen (int): rvv vector register length

    Returns:
        list: A list including 10 random int numbers between 1 and vlmax
    '''
    emul = sew/eew * factor_lmul[lmul]
    emul = int( emul if emul >= 1 else 1)
    sum = int( vlen * factor_lmul[lmul] / sew )
    esum = int ( vlen * emul / eew)
    mid = np.random.randint(2,sum-1)
    minSum = min(sum, esum)
    return list(np.unique(np.random.uniform(1, minSum, 10)).astype(int))

def get_tail_end(lmul, ebits, vlen):
    '''Function to get maximum element number of the tail part.

    Args:
        lmul (int or str): vlmul register value
        ebits (int): element bits length, which equals to vsew value.
        vlen (int): rvv register length

    Returns:
        int: The maximum element number of the tail part. When lmul >= 1, 
        the number is computed by vlen*lmul/sew. When lmul < 1, the number 
        is computed by vlen/sew.
    '''
    if factor_lmul[lmul] >= 1:
        max = int( vlen * factor_lmul[lmul] / ebits )
    else:
        max = int( vlen / ebits )
    
    return max


def get_vstart(vl):
    '''Function to get a list of int numbers to be used as vstart in test cases.

    Args:
        vl (int): vector length register value

    Returns:
        list: A list of int number between 0 and vl-1. The length of the list is computed
        by vl//10.
    '''
    return list(np.unique(np.linspace(0, vl-1, vl//10).astype(int)))    

def get_random_start(vl) :
    '''Function to get a list of 5 random int numbers between 0 and vl-1 to be used as vstart.

    Args:
        vl (int): vector length register value

    Returns:
        list: A list of 5 random int number between 0 and vl-1.
    '''
    return list(np.unique(np.random.uniform(0, vl-1, 5).astype(int)))



def get_random_stride(eew):
    '''Function to get a list of 5 random int numbers between 0 and 0xff*eew.

    Args:
        eew (int): effective element width.

    Returns:
        list: A list of 5 random int numbers between 0 and 0xff*eew. Random numbers
        are generated between 0 and 0xff first, then multiply with eew.
    '''
    return list(np.random.uniform(0, 0xff, 5).astype(int)*eew)


def vlsenn_get_stride(vl, eew, nf=1):
    '''Function to get a list of random int numbers to be used as stride of vector stride instructions.

    Args:
        vl (int): vector length register value
        eew (int): effective element length
        nf (int): nf field in vector instruction for segment instructions, default 1.

    Returns:
        list: Stride numbers are computed by 0, eew, vl*nf multiplying with eew. If nf > 1, a random int number 
        between 0 and nf and a random int number between nf+1 and 16 multiply with eew and then are appended into
        the list.
    '''
    stride_list = [0, eew*nf, vl*nf*eew]
    if nf > 1:
        stride_list.append(np.random.randint(0, nf)*eew)
        stride_list.append(np.random.randint(nf+1, 16)*eew)
    return stride_list

def get_quent_index(eew, sew, vl):
    '''Function to get consecutive indexes for index instructions.

    Args:
        eew (int): effective element width, used as index width.
        sew (int): vsew register value, used as operand element width.
        vl (int): vector length register value

    Returns:
        list: A list 2 numpy ndarray. The first array has vl size of uint 0 in eew width.
        So the indexes are 0. The second array has elements of [0, 1, ..., vl-1]*(sew//8) 
        of which the dtype is uint in eew width. They are consecutive indexes.
    '''
    index=[]
    index.append(np.zeros(vl, dtype=get_uintdtype(eew)))
    index.append(np.linspace(0, vl-1, vl, dtype=get_uintdtype(eew))*(sew//8))
    return index

def get_index(eew, sew, vl):
    '''Function to get a numpy ndarray of vl size to be used as indexes for index instructions.

    Args:
        eew (int): effective element width, used as index width.
        sew (int): vsew register value, used as operand element width.
        vl (int): vector length register value

    Returns:
        numpy ndarray:  A linspace numpy ndarray between 0 and 2**20 multiplying with sew//8 
        with size equal to vl. Its dtype is uint in eew width.
    '''
    return np.linspace(0, 2**20, vl, dtype=get_uintdtype(eew))*(sew//8)

def get_misalign_index(eew, sew, vl):
    '''Function to get misaligned indexes for index instructions.

    Args:
        eew (int): effective element width, used as index width.
        sew (int): vsew register value, used as operand element width.
        vl (int): vector length register value   

    Returns:
        numpy ndarray: A numpy ndarray, its size is vl, its elements is computed by a linspace
        array between 0 and 0xff multiplying with (sew//8)*4 and adding 3, its dtype is uint in 
        eew width.
    '''
    return np.linspace(0, 0xff, vl, dtype=get_uintdtype(eew))*(sew//8)*4+3

ld_ins = { 8: 'lbu', 16: 'lhu', 32: 'lwu', 64: 'ld'}
'''dictionary: Scalar load instructions corresponding to different widths of 8, 16, 32, 64.
'''
st_ins = { 8: 'sbu', 16: 'shu', 32: 'swu', 64: 'sd'}
'''dictionary: Scalar store instructions corresponding to different widths of 8, 16, 32, 64.
'''

def get_fldins(ebits):
    '''Function to get float load instruction corresponding to the input width.

    Args:
        ebits (int): float number width

    Returns:
        str: Float load instruction corresponding to the input width.
    '''
    return fldins_dict[ebits]

def get_fstins(ebits):
    '''Function to get float store instruction corresponding to the input width.

    Args:
        ebits (int): float number width

    Returns:
        str: Float store instruction corresponding to the input width.
    '''    
    return fstins_dict[ebits]


def get_vregister_name( lmul, neqs = 'v33', lmul_neqs = 0 ):
    '''Function to get a vector register name, which isn't overlapping with given vector register groups.

    Args:
        lmul (int or str): vmul register value.
        neqs (str or list): Given vector register or registers, default v33.
        lmul_neqs (int,str or list ): Given lmul corresponding to given vector registers. If it is equal 
            to 0, the function will use the input lmul argument as the given lmul.

    Returns:
        str: A vector register name, such as v2. The vector register group won't overlap with the given 
        vector register group.

    Raises:
        ValueError: If the length of neqs is not equal to the length of lmul_neqs.
    '''

    if not isinstance( neqs, list):
        neqs = [ neqs, ]
    if not isinstance( lmul_neqs, list ):
        lmul_neqs = [ lmul_neqs, ]
    if len(neqs) != len(lmul_neqs):
        raise ValueError("The lengths of neqs and lmul_neqs are not equal")
        return

    if isinstance( lmul, str ):
        lmul = 1

    no_neqs = []
    for no in range(len(lmul_neqs)):
        if isinstance( lmul_neqs[no], str):
            lmul_neqs[no] = 1
        if 0 == lmul_neqs[no]:
            lmul_neqs[no] = lmul
        no_neqs.append( int( neqs[no].replace( 'v', '' ) ) )

    while True:
        if isinstance(lmul, int) and lmul >= 2:
            new_no = factor_lmul[lmul] * np.random.randint(0,32/factor_lmul[lmul])            
        else:
            new_no = np.random.randint(0,32)
        
        finished = True
        for i in  range(len(lmul_neqs)):
            if ( new_no >= no_neqs[i] and new_no < ( no_neqs[i] + lmul_neqs[i] ) ) or ( no_neqs[i] >= new_no and no_neqs[i] < ( new_no + lmul )  ):
                finished = False
                break                
        if finished:
            break                
    
    return 'v'+str(new_no)


def Bitsl2Bytesl( num ):
    '''Function to transfrom bits length to corresponding bytes length.

    Args:
        num (int): Bits length.

    Returns:
        int: The length of the corresponding bytes of the input bits.
    '''
    return int(np.ceil(num/8))


def random_float(sew, vl):
    '''Function to return a numpy ndarray of random float numbers.

    Args:
        sew (int): vsew register value, float number width. It can be 16, 32, 64 corresponding to float16,
            float32 and float64.
        vl (int): vector length, the size of numpy ndarray.

    Returns:
        numpy ndarray: A numpy ndarray with random numbers in the full range of float data type. Its size is vl.
        Its dtype is float16, float32 or float64 corresponding to the input width, sew.

    Raises:
        ValueError: If sew isn't equal to 16, 32, 64.
    '''
    if sew == 16:
        num = np.random.randint( 0, 0x10000, size=vl, dtype=np.uint16 )
        num.dtype = np.float16
    elif sew == 32:
        num = np.random.randint( 0, 0x100000000, size=vl, dtype=np.uint32 )
        num.dtype = np.float32
    elif sew == 64:
        num = np.random.randint( 0, 1 << 64, size=vl, dtype=np.uint64 )
        num.dtype = np.float64        
    else:
        raise ValueError(f'{sew} is not a good option for sew.')

    return num
    
def random_int( sew, vl ):
    '''Function to return a numpy ndarray of random int numbers.

    Args:
        sew (int): vsew register value, int number width. It can be 8, 16, 32, 64 corresponding to int8, int16, 
        int32, int64.
        vl (int): vector length, the size of numpy ndarray.

    Returns:
        numpy ndarray: A numpy ndarray with random numbers in the full range of int data type. Its size is vl.
        Its dtype is int8, int16, int32 or int64 corresponding to the input width, sew.

    Raises:
        ValueError: If sew isn't equal to 8, 16, 32, 64.
    '''    
    if sew == 8:
        num = np.random.randint( 0, 0x100, size=vl, dtype=np.uint8 )
        num.dtype = np.int8
    elif sew == 16:
        num = np.random.randint( 0, 0x10000, size=vl, dtype=np.uint16 )
        num.dtype = np.int16
    elif sew == 32:
        num = np.random.randint( 0, 0x100000000, size=vl, dtype=np.uint32 )
        num.dtype = np.int32
    elif sew == 64:
        num = np.random.randint( 0, 1 << 64, size=vl, dtype=np.uint64 )
        num.dtype = np.int64        
    else:
        raise ValueError(f'{sew} is not a good option for sew.')

    return num    

def random_uint( sew, vl ):
    '''Function to return a numpy ndarray of random uint numbers.

    Args:
        sew (int): vsew register value, int number width. It can be 8, 16, 32, 64 corresponding to uint8, uint16, 
        uint32, uint64.
        vl (int): vector length, the size of numpy ndarray.

    Returns:
        numpy ndarray: A numpy ndarray with random numbers in the full range of uint data type. Its size is vl.
        Its dtype is uint8, uint16, uint32 or uint64 corresponding to the input width, sew.

    Raises:
        ValueError: If sew isn't equal to 8, 16, 32, 64.
    '''      
    if sew == 8:
        num = np.random.randint( 0, 0x100, size=vl, dtype=np.uint8 )
    elif sew == 16:
        num = np.random.randint( 0, 0x10000, size=vl, dtype=np.uint16 )
    elif sew == 32:
        num = np.random.randint( 0, 0x100000000, size=vl, dtype=np.uint32 )
    elif sew == 64:
        num = np.random.randint( 0, 1 << 64, size=vl, dtype=np.uint64 )       
    else:
        raise ValueError(f'{sew} is not a good option for sew.')

    return num

