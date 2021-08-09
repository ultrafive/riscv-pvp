import numpy as np
import random
import pytest

def linspace_mm(type, w, h):
    return [
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
    ]

def linspace_mm_stride(type, w, h, dstride, sstride1, sstride2 ):
    return [
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        dstride,
        sstride1,
        sstride2,
    ]

def linspace_mm_rs1_eq_rs2(type, w, h):
    return [
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h),  
    ]

def special_float_mm(type, w, h):
    # special float table        -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    fpt0 = np.array([[0x0000]*6, [0x8000, 0x7c00,         0x7e00,                 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt1 = np.array([[0x7c00]*8, [        0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt2 = np.array([[0x7e00]*6, [                        0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt3 = np.array([[0x2e66]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt4 = np.array([[0x4900]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt5 = np.array([[0x7bff]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt6 = np.array([[0x0400]*2, [                                                        0x0400, 0x0001]], dtype=np.int16)
    fpt7 = np.array([[0x0001]*1, [                                                                0x0001]], dtype=np.int16)
    fpt_data = np.concatenate((fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7),axis=1)
    fpt_data.dtype = type

    return [
        fpt_data[0].reshape(w, h), 
        fpt_data[1].reshape(w, h),
    ]

def linespace_mv( type, w, h, dim_h ):
    rs1 = np.linspace(-127, 200, w*h, dtype=type).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return [
        rs1, 
        vs2,
        dim_h,
    ]

def linespace_mv_stride( type, w, h, dim_h, dstride, sstride1 ):
    rs1 = np.linspace(-127, 200, w*h, dtype=type).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return [
        rs1, 
        vs2,
        dim_h,
        dstride,
        sstride1,
    ]

def linespace_mv_x32( type, w, h, dim_h ):
    rs1 = np.linspace(-127, 200, w*h, dtype=np.int32).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return [
        rs1, 
        vs2,
        dim_h,
    ]

def linespace_mv_stride_x32( type, w, h, dim_h, dstride, sstride1 ):
    rs1 = np.linspace(-127, 200, w*h, dtype=np.int32).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return [
        rs1, 
        vs2,
        dim_h,
        dstride,
        sstride1,
    ]

def special_float_mv(type, w, h, dim_h):
    # special float table        -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    fpt0 = np.array([[0x0000]*6, [0x8000, 0x7c00,         0x7e00,                 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt1 = np.array([[0x7c00]*8, [        0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt2 = np.array([[0x7e00]*6, [                        0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt3 = np.array([[0x2e66]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt4 = np.array([[0x4900]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt5 = np.array([[0x7bff]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    fpt6 = np.array([[0x0400]*2, [                                                        0x0400, 0x0001]], dtype=np.int16)
    fpt7 = np.array([[0x0001]*1, [                                                                0x0001]], dtype=np.int16)
    fpt_data = np.concatenate((fpt0, fpt1, fpt2, fpt3, fpt4, fpt5, fpt6, fpt7),axis=1)
    fpt_data.dtype = type

    return [
        fpt_data[0].reshape(h, w), 
        fpt_data[1].reshape(h, w),
        dim_h,
    ]

def random_mf( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    return [
        rs1,
        rs2,
    ]

def random_mf_stride( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    return [
        rs1,
        rs2,
        stride_s1,
        stride_rd,
    ]

def random_mf_x32( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs1 = (rs1 * np.iinfo(np.int8).max).astype(np.int32)
    rs2 = np.random.random((1, 1)).astype('float32')
    return [
        rs1,
        rs2,
    ]

def random_mf_stride_x32( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs1 = (rs1 * np.iinfo(np.int8).max).astype(np.int32)
    rs2 = np.random.random((1, 1)).astype('float32')
    return [
        rs1,
        rs2,
        stride_s1,
        stride_rd,
    ]

def random_mf_x8_hf( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    rs2 = rs2 * 128
    return [
        rs1,
        rs2,
    ]

def random_mf_stride_x8_hf( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    rs2 = rs2 * 128
    return [
        rs1,
        rs2,
        stride_s1,
        stride_rd,
    ]

def random_m( dtype, width, height ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return [
        rs1,
    ]

def random_m_stride( dtype, width, height, sstride1 ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return [
        rs1,
        sstride1,
    ]

def special_float_m( dtype, num, special_hex ):
    s1 = np.linspace( -1, 1, 256, dtype=dtype ).reshape( 16, 16 )
    sa = np.array( [special_hex], dtype=np.int16 )
    sa.dtype = dtype
    s1[num % 15][6] = sa[0]

    return [
        s1,
    ]

def random_m_dim( dtype, width, height, dim ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return [
        rs1,
        dim,
    ]

def random_m_stride_dim( dtype, width, height, sstride1, dim ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return [
        rs1,
        sstride1,
        dim,
    ]

def special_float_m_dim( dtype, num, special_hex, dim ):
    s1 = np.linspace( -1, 1, 256, dtype=dtype ).reshape( 16, 16 )
    sa = np.array( [special_hex], dtype=np.int16 )
    sa.dtype = dtype
    s1[num % 15][6] = sa[0]

    return [
        s1,
        dim,
    ]

def ramdom_veemacc_mm_all_sum( height, width ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return [
        rs1, 
        rs2,
    ]

def ramdom_veemacc_mm_all_sum_stride( height, width, stride_s1, stride_s2 ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return [
        rs1, 
        rs2,
        stride_s1,
        stride_s2,
    ]

def ramdom_veemacc_mm( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return [
        rs1, 
        rs2,
        dim, 
    ]

def ramdom_veemacc_mm_stride( height, width, stride_s1, stride_s2, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return [
        rs1, 
        rs2,
        stride_s1,
        stride_s2,
        dim,
    ]

def ramdom_veemacc_mm_overlap( height, width, overlap_addr, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return [
        rs1, 
        rs2,
        overlap_addr,
        dim,
    ]

def ramdom_veemacc_mv( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return [
        rs1, 
        rs2,
        dim,
    ]

def ramdom_veemacc_mv_stride( height, width, stride_s1, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return [
        rs1, 
        rs2,
        stride_s1,
        dim,
    ]

def ramdom_veemacc_mv_overlap( height, width, overlap_addr, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return [
        rs1, 
        rs2,
        overlap_addr,
        dim,
    ]

def ramdom_veemacc_mf( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((1, 1)).astype('float32')

    return [
        rs1, 
        rs2,
        dim,
    ]

def ramdom_veemacc_mf_stride( height, width, stride_s1, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((1, 1)).astype('float32')

    return [
        rs1, 
        rs2,
        stride_s1,
        dim,
    ]

def linspace_xx_m( start, stop, stype, height, width ):
    rs1 = np.linspace( start=start, stop=stop, num=width*height, dtype=stype ).reshape( height, width )
    return rs1

def linspace_xx_m_stride( start, stop, stype, height, width, stride_rd, stride_s1 ):
    rs1 = np.linspace( start=start, stop=stop, num=width*height, dtype=stype ).reshape( height, width )
    return [  rs1, stride_rd, stride_s1 ]

def special_float_xx_m( stype, height, width ):
    # special float table 1, -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    rs1 = np.array([0x3c00,    0x8000, 0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001], dtype=np.int16)
    rs1.dtype=stype
    rs1.reshape(2, 5)
    return [
        rs1, 
    ]

def metr_m( height, weight ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return [
        rs,
    ]

def metr_m_stride( height, weight, stride_s, stride_d ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return [
        rs,
        stride_s,
        stride_d,
    ]

def metr_m_misaligned_block( height, weight, off_s, off_d ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return [
        rs,
        off_s,
        off_d,
    ]

def random_memul_mm( l ):
    [ lb, ub, m, k, n] = l
    vs1 = np.random.random((m, k)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2 ]

def random_memul_mm_stride( l ):
    [ lb, ub, m, k, n, stride_s1, stride_s2, stride_d ] = l
    vs1 = np.random.random((m, k)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2, stride_s1, stride_s2, stride_d ]

def random_memul_mm_misaligned_block( l ):
    [ lb, ub, m, k, n, off_s1, off_s2, off_d ] = l
    vs1 = np.random.random((m, k)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2, off_s1, off_s2, off_d ]

def softfloat_memul_mm( l ):
    [ lb, ub, m, k, n] = l
    vs1 = np.array( [np.half('inf'), np.half('-inf'), 0, np.half('nan')], dtype=np.float16 ).reshape( m, k )
    vs2 = np.array( [np.half('inf'), np.half('-inf'), 0, np.half('nan')], dtype=np.float16).reshape( k, n )
    return [ vs1, vs2 ]

def random_memul_ts_mm( l ):
    [ lb, ub, m, k, n] = l
    vs1 = np.random.random((k, m)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2 ]

def random_memul_ts_mm_stride( l ):
    [ lb, ub, m, k, n, stride_s1, stride_s2, stride_d ] = l
    vs1 = np.random.random((k, m)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2, stride_s1, stride_s2, stride_d ]

def random_memul_ts_mm_misaligned_block( l ):
    [ lb, ub, m, k, n, off_s1, off_s2, off_d ] = l
    vs1 = np.random.random((k, m)).astype('float16') * ( ub - lb ) + lb
    vs2 = np.random.random((k, n)).astype('float16') * ( ub - lb ) + lb
    return [ vs1, vs2, off_s1, off_s2, off_d ]

def softfloat_memul_ts_mm( l ):
    [ lb, ub, m, k, n] = l
    vs1 = np.array( [np.half('inf'), np.half('-inf'), 0, np.half('nan')], dtype=np.float16 ).reshape( k, m )
    vs2 = np.array( [np.half('inf'), np.half('-inf'), 0, np.half('nan')], dtype=np.float16).reshape( k, n )
    return [ vs1, vs2 ]

def random_memul_x8_mm( l ):
    [ lb, ub, m, k, n] = l
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ vs1, vs2 ]

def random_memul_x8_mm_stride( l ):
    [ lb, ub, m, k, n, stride_s1, stride_s2, stride_d ] = l
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ vs1, vs2, stride_s1, stride_s2, stride_d ]

def random_memul_x8_mm_misaligned_block( l ):
    [ lb, ub, m, k, n, off_s1, off_s2, off_d ] = l
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ vs1, vs2, off_s1, off_s2, off_d ]

def random_memul_hf_x8_mm( l ):
    [ lb, ub, m, k, n] = l
    dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2 ]

def random_memul_hf_x8_mm_stride( l ):
    [ lb, ub, m, k, n, stride_s1, stride_s2, stride_d ] = l
    dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2, stride_s1, stride_s2, stride_d ] 

def random_memul_hf_x8_mm_misaligned_block( l ):
    [ lb, ub, m, k, n, off_s1, off_s2, off_d ] = l
    dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2, off_s1, off_s2, off_d ]

def softfloat_hf_x8_mm(l):
    [ lb, ub, m, k, n, dequant_ ] = l
    dequant = np.array([1], dtype=np.float32)
    dequant.fill(dequant_)
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((k, n)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2 ]

def random_velkrelu_mv( height, width, vl, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vl ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return [ 
        rs1, 
        rs2,
        dim_flag,
    ]

def random_velkrelu_special_mv( height, width, vl, dim_flag ):
    special_fp16_less_eq_zero = np.array([0, 0.0, np.half('inf'), np.half('-inf'), np.half('nan'), 0.1, 10, 65500, 6.104e-5], dtype=np.float16)
    rs1 = special_fp16_less_eq_zero;
    cnt = special_fp16_less_eq_zero.size
    for x in range(cnt-1):
        tmp=np.roll(special_fp16_less_eq_zero, 1)
        rs1=np.append(rs1, tmp)
        special_fp16_less_eq_zero =tmp
    rs1 = np.reshape(rs1, (cnt, cnt))
    rs2 = np.array([0.1, 0.1, np.half('nan'), 0.1, 10, 65500, 6.104e-5, 6e-8, -1.0], dtype=np.float16)

    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return [ 
        rs1, 
        rs2,
        dim_flag,
    ]

def random_velkrelu_stride_mv( height, width, vl, stride_s, stride_d, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vl ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return [ 
        rs1, 
        rs2,
        dim_flag,
        stride_s, 
        stride_d,
    ]

def random_velkrelu_misaligned_mv( height, width, vl, offset, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vl ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return [ 
        rs1, 
        rs2,
        dim_flag,
        offset,
    ]

def random_velut_m( width, height, tsize ):
    rs1 = np.random.randint( 29, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 30 ).astype( np.half )
    return [
        rs1, 
        rs2,
        tsize,
    ]

def random_velut_m_full_fill_l1b( width, height, tsize ):
    rs1 = np.random.randint( 64 * 1024 - 1, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 64 * 1024 ).astype( np.half )
    return [
        rs1, 
        rs2,
        tsize,
    ]

def random_velut_m_special( width, height, tsize ):
    # special float table   0,    -0,     inf,   -inf,    nan,    0.1,   10,    65500,  6.104e-05, 6.e-08
    rs1 = np.array( [0000, 0x8000, 0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff,  0x0400,    0x0001], dtype=np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace(-3.0, 3.0, 0xfc01).astype(np.half)
    return [
        rs1, 
        rs2,
        tsize,
    ]

def random_velut_m_stride( width, height, tsize, dstride, sstride ):
    rs1 = np.random.randint( 29, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 30 ).astype( np.half )
    return [
        rs1, 
        rs2,
        tsize,
        dstride,
        sstride,
    ]

def random_meconv_mm( h, w, cin, cout, kh, kw, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        padding,
        sk,
        dl,
    ]

def random_meconv_mm_stride( h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        stride_s1,
        stride_s2,
        stride_d,
        padding,
        sk,
        dl,
    ]

def random_meconv_mm_misaligned_block( h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        off_s1,
        off_s2,
        off_d,
        padding,
        sk,
        dl,
    ]

def meconv_mm_special_fp( h, w, cin, cout, kh, kw, padding, sk, dl ):
    vs1 = np.array([0.0, -0.0, np.half('inf'), np.half('-inf'), np.half('nan'),
                    0.1, 10, 65500, 6.104e-05, 6.e-08], dtype=np.float16).reshape((1, 1, 10, 1))
    vs2 = np.array([0.0, -0.0, np.half('inf'), np.half('-inf'), np.half('nan'),
                    0.1, 10, 65500, 6.104e-05, 6.e-08], dtype=np.float16).reshape((1, 1, 1, 10))
    return [
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        padding,
        sk,
        dl,
    ]

def random_meconv_x8_mm( h, w, cin, cout, kh, kw, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        padding,
        sk,
        dl,
    ]

def random_meconv_x8_mm_stride( h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        stride_s1,
        stride_s2,
        stride_d,
        padding,
        sk,
        dl,
    ]

def random_meconv_x8_mm_misaligned_block( h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        off_s1,
        off_s2,
        off_d,
        padding,
        sk,
        dl,
    ]

def random_meconv_hf_x8_mm( h, w, cin, cout, kh, kw, padding, sk, dl, dequant_fp=None ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    if not dequant_fp:
        dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    else:
        dequant = np.array([1], dtype=np.float32)
        dequant.fill(dequant_fp)
    vs1 = (np.random.random(shape_input) * (256) - 128).astype('int8')
    vs2 = (np.random.random(shape_filter) * (256) - 128).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        padding,
        sk,
        dl,
        dequant,
    ]

def random_meconv_hf_x8_mm_stride( h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl, dequant_fp=None ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    if not dequant_fp:
        dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    else:
        dequant = np.array([1], dtype=np.float32)
        dequant.fill(dequant_fp)
    vs1 = (np.random.random(shape_input) * (256) - 128).astype('int8')
    vs2 = (np.random.random(shape_filter) * (256) - 128).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        stride_s1,
        stride_s2,
        stride_d,
        padding,
        sk,
        dl,
        dequant, 
    ]

def random_meconv_hf_x8_mm_misaligned_block( h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl, dequant_fp=None ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    if not dequant_fp:
        dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    else:
        dequant = np.array([1], dtype=np.float32)
        dequant.fill(dequant_fp)
    vs1 = (np.random.random(shape_input) * (256) - 128).astype('int8')
    vs2 = (np.random.random(shape_filter) * (256) - 128).astype('int8')
    return [ 
        vs1, 
        vs2,
        h,
        w,
        cin,
        cout,
        kh,
        kw,
        off_s1,
        off_s2,
        off_d,
        padding,
        sk,
        dl,
        dequant,
    ]

def rvv_v_generator(vl, dtype=np.int16):
    return np.linspace(1, 0xffff, vl, dtype=dtype)

def linspace_rvv_vv(type, vl):
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_wv(type, vl):
    if type == np.float16:
        type_vs2 = np.float32
    elif type == np.float32:
        type_vs2 = np.float64
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type_vs2)
    ]

def linspace_rvv_m_v(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-127, 128, vl, dtype=type_vd),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_vf(type, vl):
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-127, 128, vl, dtype=type)
    ]

def linspace_rvv_m_vf_w(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-5, 5, vl, dtype=type_vd),
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_wf(type, vl):
    if type == np.float16:
        type_vs2 = np.float32
    elif type == np.float32:
        type_vs2 = np.float64
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-127, 128, vl, dtype=type_vs2)
    ]

def linspace_rvv_vvv(type, vl):
    return [
        np.linspace(-5, 5, vl, dtype=type),
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_m_vv_w(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-5, 5, vl, dtype=type_vd),
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_vvv_wred(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-5, 5, vl, dtype=type_vd),
        np.linspace(-127, 128, vl, dtype=type_vd),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_vv_wred(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-127, 128, vl, dtype=type_vd),
        np.linspace(-120, 135, vl, dtype=type)
    ]

def linspace_rvv_m_vf(type, vl):
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.array(random.random(), dtype=type),
        np.linspace(-120, 135, vl, dtype=type)
    ]
def random_mask( vl ):
    return np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int16)), dtype=np.uint8)

def random_e1( vl ):
    return np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.uint8)), dtype=np.uint8)

def res_len_e1( vl ):
    return np.ceil( vl/8 ).astype( np.uint8 )


def linspace_rvv_vv_with_mask(type, vl):

    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type),
        vl
    ]

def linspace_rvv_vf_with_mask(type, vl):
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type),
        vl
    ]

def linspace_rvv_slide1up_vf_with_mask(type, vl, fmask):
    mask = np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8)
    if fmask:
        mask[0] = mask[0] | 1
    else:
        mask[0] = mask[0] & 0xFE
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        mask,
        np.linspace(-1, 1, vl, dtype=type), 
        vl
    ]

def linspace_rvv_slide1down_vf_with_mask(type, vl, fmask):
    mask = np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8)
    idx = int( np.floor( (vl-1)/8 ) )
    bitx= (vl-1) % 8
    if fmask:
        mask[idx] = mask[idx] | ( 1 << bitx )
    else:
        mask[idx] = mask[idx] & ( 0xFF - ( 1<<bitx ) )

    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        mask,
        np.linspace(-1, 1, vl, dtype=type),
        vl
    ]

def linspace_rvv_wf_with_mask(type, vl):
    if type == np.float16:
        type_vs2 = np.float32
    elif type == np.float32:
        type_vs2 = np.float64
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type_vs2),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type_vs2),
        vl
    ]

def linspace_rvv_m_vv_with_mask(type, vl):
    return [
        np.linspace(-1, 1, vl, dtype=type),
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        vl
    ]
def linspace_rvv_m_vf_with_mask(type, vl):
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        vl
    ]
def linspace_rvv_vv_w_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type_vd),
        vl
    ]
def linspace_rvv_m_vv_w_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-1, 1, vl, dtype=type_vd),        
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        vl
    ]

def linspace_rvv_wred_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-1, 1, vl, dtype=type_vd),        
        np.linspace(-127, 128, vl, dtype=type_vd),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8)
    ]

def linspace_rvv_m_vf_w_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-1, 1, vl, dtype=type_vd),        
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        vl
    ]

def linspace_rvv_vf_w_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.array(random.random(), dtype=np.float32),
        np.linspace(-120, 135, vl, dtype=type),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type_vd),
        vl
    ]

def linspace_rvv_wv_w_with_mask(type, vl):
    if type == np.float16:
        type_vd = np.float32
    elif type == np.float32:
        type_vd = np.float64
    return [
        np.linspace(-127, 128, vl, dtype=type),
        np.linspace(-120, 135, vl, dtype=type_vd),
        np.array( np.random.randint( 0, 255, np.ceil(vl/8).astype(np.int8)), dtype=np.uint8),
        np.linspace(-1, 1, vl, dtype=type_vd),
        vl
    ]
#special vector data
def linspace_rvv_v_special(type, offset, vl):
    # boundary number table        -0   ,  inf  ,  -inf ,  nan  ,  0.1  ,  10  ,  65500 , 6.104e-05, 6.e-08
    bd0 = np.array([[0x0000]*6, [0x0000, 0x7c00,         0x7e00,                 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd1 = np.array([[0x7c00]*8, [        0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd2 = np.array([[0x7e00]*6, [                        0x7e00, 0x2e66, 0x4900, 0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd3 = np.array([[0x2e66]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd4 = np.array([[0x4900]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd5 = np.array([[0x7bff]*3, [                                                0x7bff, 0x0400, 0x0001]], dtype=np.int16)
    bd6 = np.array([[0x0400]*2, [                                                        0x0400, 0x0001]], dtype=np.int16)
    bd7 = np.array([[0x0001]*1, [                                                                0x0001]], dtype=np.int16)
    bound_data = np.concatenate((bd0, bd1, bd2, bd3, bd4, bd5, bd6, bd7),axis=1)
    bound_data.dtype = type

    # vs data include boundary data, vl is 64
    vs = np.linspace(-1, 5, vl, dtype=type)
    if offset > 1:
        offset = 1;
    vs[:len(bound_data[offset])] = bound_data[offset]

    return vs


def packbits(a):
    return np.packbits(np.array(a, dtype=np.uint8), bitorder='little')

def special_vv_fp16():
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

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

def get_vl(lmul, ebits, vlen):
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
    max = int( vlen * factor_lmul[lmul] / ebits )
    return max

def vlsenn_get_stride(vl, align):
    vl = int(vl)
    align = int(align)

    if vl/align < 1:
        return [ 0, align ]
    if vl/align < 2:
        return [ 0, align, 2*align]
    if vl/align < 3:
        return [ 0, align, 2*align, 3*align]

    vl_factor = int(np.floor(vl/align))
    mid = int(np.random.randint(2, vl_factor))
    return [ 0, align, mid*align, vl_factor*align, (vl_factor+1)*align] 

def get_lmul(sew):
    if 8 == sew:
        return [1,2,4,8,'f2','f4','f8']
    if 16 == sew:
        return [1,2,4,8,'f2','f4']
    if 32 == sew:
        return [1,2,4,8,'f2']
    if 64 == sew:
        return [1,2,4,8]

def get_lmul_seg(sew):
    if 8 == sew:
        return [1,2,4,'f2','f4','f8']
    if 16 == sew:
        return [1,2,4,'f2','f4']
    if 32 == sew:
        return [1,2,4,'f2']
    if 64 == sew:
        return [1,2,4]    

def get_nfields(lmul):
    if lmul == 1:
        return [ 2, 3, 4, 5, 6, 7, 8]
    if lmul == 2:
        return [ 2, 3, 4 ]
    if lmul == 4:
        return [ 2 ]
    if lmul == 8:
        return None
    else:
        return [ 2, 3, 4, 5, 6, 7, 8]

def get_intdtype(sew):
    int_dtype_dict = { 8: np.int8, 16: np.int16, 32: np.int32, 64: np.int64 }
    return int_dtype_dict[sew]

def get_floatdtype(sew):
    float_dtype_dict = { 16: np.float16, 32: np.float32, 64: np.float64 }
    return float_dtype_dict[sew]

def get_float_pos_min(sew):

    if sew == 16:
        num = np.array( [0x1], dtype=np.uint16 )
        num.dtype = np.float16
    elif sew == 32:
        num = np.array( [0x1], dtype=np.uint32)
        num.dtype = np.float32
    elif sew == 64:
        num = np.array( [0x1], dtype=np.uint64)
        num.dtype = np.float64
    else:
        raise ValueError(f"{sew} is not a good option for sew")

    return num
 

def get_float_max(sew):

    if sew == 16:
        num = np.array( [0x7BFF], dtype=np.uint16 )
        num.dtype = np.float16
    elif sew == 32:
        num = np.array( [0x7F7FFFFF], dtype=np.uint32)
        num.dtype = np.float32
    elif sew == 64:
        num = np.array( [0x7FEFFFFFFFFFFFFF], dtype=np.uint64)
        num.dtype = np.float64
    else:
        raise ValueError(f"{sew} is not a good option for sew.")        

    return num

def random_float(sew, vl):
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
