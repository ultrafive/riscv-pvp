import numpy as np

fldins_dict = { 16: "flh", 32: "flw", 64: "fld" }
fstins_dict = { 16: "fsh", 32: "fsw", 64: "fsd" }
load_inst_dict = { 8: 'lbu', 16: 'lhu', 32: 'lwu', 64: 'ld'}
store_inst_dict = { 8: 'sbu', 16: 'shu', 32: 'swu', 64: 'sd'}

factor_lmul = { 1:1, "1":1, 2:2, "2":2, 4:4, "4":4, 8:8, "8":8, 'f2':0.5, 'f4':0.25, 'f8':0.125}
string_lmul = { 1:1, 2:2, 4:4, 8:8, 0.5:'f2', 0.25:'f4', 0.125:'f8'}

def vector_widen_lmul(lmul):
    '''Function to compute double lmul value of input lmul.

    Args:
        lmul (int or str): lmul register value, which can be 1, 2, 4, '1', '2', '4', 'f2', 'f4', 'f8'

    Returns:
        int or str: double lmul value
    '''
    vector_widen_lmul_dict = {1:2, "1":2, 2:4, "2":4, 4:8, "4":8, 'f2':1, 'f4':'f2', 'f8':'f4'}
    return vector_widen_lmul_dict[lmul]

def vector_emul(eew, sew, lmul):
    '''Function to get emul based on sew, eew and lmul.

    Args:
        eew (int): effective element width 
        sew (int): selected element width
        lmul (int or str): vlmul register value

    Returns:
        int or str: computed emul value based eew/sew = emul/lmul

    '''
    return string_lmul[ (eew/sew)*factor_lmul[lmul] ]

def vector_vlmax(lmul, ebits, vlen):
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

def vector_len_vreg_aligned(lmul, ebits, vlen):
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

def bits_to_dtype_int(sew):
    '''Function to get int data type corresponding the input width.

    Args:
        sew (int): vsew register value, int data width, which can be 8, 16, 32, 64.

    Returns:
        dtype: numpy int dtype corresponding to the data width, numpy.int8 corresponding to 8,
        numpy.int16 corresponding to 16, numpy.int32 corresponding to 32, numpy.int64 corresponding to 64.
    '''
    int_dtype_dict = { 8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64 }
    return int_dtype_dict[sew]

def bits_to_dtype_uint(sew):
    '''Function to get uint data type corresponding the input width.

    Args:
        sew (int): vsew register value, uint data width, which can be 8, 16, 32, 64.

    Returns:
        dtype: numpy uint dtype corresponding to the data width, numpy.uint8 corresponding to 8,
        numpy.uint16 corresponding to 16, numpy.uint32 corresponding to 32, numpy.uint64 corresponding to 64.
    '''    
    uint_dtype_dict = { 8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64 }
    return uint_dtype_dict[sew]    

def bits_to_dtype_float(sew):
    '''Function to get float data type corresponding the input width.

    Args:
        sew (int): vsew register value, float data width, which can be 16, 32, 64.

    Returns:
        dtype: numpy float dtype corresponding to the data width, numpy.float16 corresponding to 16,
        numpy.float32 corresponding to 32, numpy.float64 corresponding to 64.
    '''    
    float_dtype_dict = { 16: np.float16, 32: np.float32, 64: np.float64 }
    return float_dtype_dict[sew]

def bits_to_bytes( num ):
    '''Function to transfrom bits length to corresponding bytes length.

    Args:
        num (int): Bits length.

    Returns:
        int: The length of the corresponding bytes of the input bits.
    '''
    return int(np.ceil(num/8))

def bits_to_intmin(sew):
    '''Function to get the minimum value in int data type.

    Args:
        sew (int): data width

    Returns:
        int: The minimum value in int data type of sew width.
    '''
    return -(2**(sew-1))

def bits_to_intmax(sew):
    '''Function to get the maximum value in int data type.

    Args:
        sew (int): data width

    Returns:
        int: The maximum value in int data type of sew width.
    '''    
    return 2**(sew-1)-1

def bits_to_uintmax(sew):
    '''Function to get the maximum value in uint data type.

    Args:
        sew (int): data width

    Returns:
        int: The maximum value in uint data type of sew width.
    '''    
    return 2**sew-1

def hex_to_fp16( num ):
    '''Function to transform a hex uint16 number to corresponding float16 number.

    Args:
        num (uint16): The input number need to be transformed.

    Returns:
        float16: The transformed float16 number from the input number.
    '''
    num = np.array([num], dtype = np.uint16  )
    num.dtype = np.float16
    return num

def hex_to_fp32( num ):
    '''Function to transform a hex uint32 number to corresponding float32 number.

    Args:
        num (uint32): The input number need to be transformed.

    Returns:
        float32: The transformed float32 number from the input number.
    '''    
    num = np.array([num], dtype = np.uint32  )
    num.dtype = np.float32
    return num

def hex_to_fp64( num ):
    '''Function to transform a hex uint64 number to corresponding float64 number.

    Args:
        num (uint64): The input number need to be transformed.

    Returns:
        float64: The transformed float64 number from the input number.
    '''    
    num = np.array([num], dtype = np.uint64  )
    num.dtype = np.float64
    return num        


def copy_to_dtype( input, dtype ):
    '''Function to copy the input numpy ndarray's dtype to the target dtype, which doesn't change the bytes, just
    change the bytes interpreting method.

    Args:
        input (numpy ndarray): The input numpy ndarray need to be transformed.
        dtype (numpy dtype): The target numpy dtype.

    Returns:
        numpy ndarray: The transformed numpy ndarray in the target dtype.
    '''
    output = input.copy()
    if output.shape == ():
        output = output.reshape(1,)
    output.dtype = dtype
    return output

def load_inst(ebits):
    '''Function to get load instruction corresponding to the input width.

    Args:
        ebits (int): data width

    Returns:
        str: Float load instruction corresponding to the input width.
    '''
    return load_inst_dict[ebits]

def store_inst(ebits):
    '''Function to get store instruction corresponding to the input width.

    Args:
        ebits (int): data width

    Returns:
        str: Float store instruction corresponding to the input width.
    '''
    return store_inst_dict[ebits]

def fload_inst(ebits):
    '''Function to get float load instruction corresponding to the input width.

    Args:
        ebits (int): float number width

    Returns:
        str: Float load instruction corresponding to the input width.
    '''
    return fldins_dict[ebits]

def fstore_inst(ebits):
    '''Function to get float store instruction corresponding to the input width.

    Args:
        ebits (int): float number width

    Returns:
        str: Float store instruction corresponding to the input width.
    '''    
    return fstins_dict[ebits]

def alloc_vreg( lmul, neqs = 'v33', lmul_neqs = 0 ):
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