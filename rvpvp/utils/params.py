import numpy as np

factor_lmul = { 1:1, "1":1, 2:2, "2":2, 4:4, "4":4, 8:8, "8":8, 'f2':0.5, 'f4':0.25, 'f8':0.125}
'''dictionary: factors corresponding to different lmul
'''

double_lmul_dict = {1:2, "1":2, 2:4, "2":4, 4:8, "4":8, 'f2':1, 'f4':'f2', 'f8':'f4'}
'''dictionary: double lmul corresponding to different lmul
'''

string_lmul = { 1:1, 2:2, 4:4, 8:8, 0.5:'f2', 0.25:'f4', 0.125:'f8'}
'''dictionary: lmul corresponding to different lmul factor
'''

fldins_dict = { 16: "flh", 32: "flw", 64: "fld" }
'''dictionary: float load instructions corresponding to different widths
'''

fstins_dict = { 16: "fsh", 32: "fsw", 64: "fsd" }
'''dictionary: float store instructions corresponding to different widths
'''

def get_intdtype(sew):
    '''Function to get int data type corresponding the input width.

    Args:
        sew (int): vsew register value, int data width, which can be 8, 16, 32, 64.

    Returns:
        dtype: numpy int dtype corresponding to the data width, numpy.int8 corresponding to 8,
        numpy.int16 corresponding to 16, numpy.int32 corresponding to 32, numpy.int64 corresponding to 64.
    '''
    int_dtype_dict = { 8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64 }
    return int_dtype_dict[sew]

def get_uintdtype(sew):
    '''Function to get uint data type corresponding the input width.

    Args:
        sew (int): vsew register value, uint data width, which can be 8, 16, 32, 64.

    Returns:
        dtype: numpy uint dtype corresponding to the data width, numpy.uint8 corresponding to 8,
        numpy.uint16 corresponding to 16, numpy.uint32 corresponding to 32, numpy.uint64 corresponding to 64.
    '''    
    uint_dtype_dict = { 8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64 }
    return uint_dtype_dict[sew]    

def get_floatdtype(sew):
    '''Function to get float data type corresponding the input width.

    Args:
        sew (int): vsew register value, float data width, which can be 16, 32, 64.

    Returns:
        dtype: numpy float dtype corresponding to the data width, numpy.float16 corresponding to 16,
        numpy.float32 corresponding to 32, numpy.float64 corresponding to 64.
    '''    
    float_dtype_dict = { 16: np.float16, 32: np.float32, 64: np.float64 }
    return float_dtype_dict[sew]

def get_intmin(sew):
    '''Function to get the minimum value in int data type.

    Args:
        sew (int): data width

    Returns:
        int: The minimum value in int data type of sew width.
    '''
    return -(2**(sew-1))

def get_intmax(sew):
    '''Function to get the maximum value in int data type.

    Args:
        sew (int): data width

    Returns:
        int: The maximum value in int data type of sew width.
    '''    
    return 2**(sew-1)-1

def get_uintmax(sew):
    '''Function to get the maximum value in uint data type.

    Args:
        sew (int): data width

    Returns:
        int: The maximum value in uint data type of sew width.
    '''    
    return 2**sew-1

def hex2fp16( num ):
    '''Function to transform a hex uint16 number to corresponding float16 number.

    Args:
        num (uint16): The input number need to be transformed.

    Returns:
        float16: The transformed float16 number from the input number.
    '''
    num = np.array([num], dtype = np.uint16  )
    num.dtype = np.float16
    return num

def hex2fp32( num ):
    '''Function to transform a hex uint32 number to corresponding float32 number.

    Args:
        num (uint32): The input number need to be transformed.

    Returns:
        float32: The transformed float32 number from the input number.
    '''    
    num = np.array([num], dtype = np.uint32  )
    num.dtype = np.float32
    return num

def hex2fp64( num ):
    '''Function to transform a hex uint64 number to corresponding float64 number.

    Args:
        num (uint64): The input number need to be transformed.

    Returns:
        float64: The transformed float64 number from the input number.
    '''    
    num = np.array([num], dtype = np.uint64  )
    num.dtype = np.float64
    return num        


def trans_dtype( input, dtype ):
    '''Function to transform the input numpy ndarray's dtype to the target dtype, which doesn't change the bytes, just
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