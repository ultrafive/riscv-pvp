import numpy as np
import pytest

def linspace_mm(type, w, h):
    return pytest.param(
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        id=f'{w}x{h}'
    )

def linspace_mm_stride(type, w, h, dstride, sstride1, sstride2 ):
    return pytest.param(
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        dstride,
        sstride1,
        sstride2,
        id=f'{w}x{h}'
    )

def linspace_mm_rs1_eq_rs2(type, w, h):
    return pytest.param(
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h),  
        id=f'{w}x{h}'
    )

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

    return pytest.param(
        fpt_data[0].reshape(w, h), 
        fpt_data[1].reshape(w, h),
        id=f'{w}x{h}'
    )

def linespace_mv( type, w, h, dim_h ):
    rs1 = np.linspace(-127, 200, w*h, dtype=type).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return pytest.param(
        rs1, 
        vs2,
        dim_h,
        id=f'{w}x{h}x{dim_h}'
    )

def linespace_mv_stride( type, w, h, dim_h, dstride, sstride1 ):
    rs1 = np.linspace(-127, 200, w*h, dtype=type).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return pytest.param(
        rs1, 
        vs2,
        dim_h,
        dstride,
        sstride1,
        id=f'{w}x{h}x{dim_h}x{dstride}x{sstride1}'
    )

def linespace_mv_x32( type, w, h, dim_h ):
    rs1 = np.linspace(-127, 200, w*h, dtype=np.int32).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return pytest.param(
        rs1, 
        vs2,
        dim_h,
        id=f'{w}x{h}x{dim_h}'
    )

def linespace_mv_stride_x32( type, w, h, dim_h, dstride, sstride1 ):
    rs1 = np.linspace(-127, 200, w*h, dtype=np.int32).reshape(h, w)
    if dim_h:
        vs2 = np.linspace(300, 40, w, dtype=type).reshape(1, w)
    else:
        vs2 = np.linspace(300, 40, h, dtype=type).reshape(h, 1)
    return pytest.param(
        rs1, 
        vs2,
        dim_h,
        dstride,
        sstride1,
        id=f'{w}x{h}x{dim_h}x{dstride}x{sstride1}'
    )

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

    return pytest.param(
        fpt_data[0].reshape(h, w), 
        fpt_data[1].reshape(h, w),
        dim_h,
        id=f'{dim_h}'
    )

def random_mf( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    return pytest.param(
        rs1,
        rs2,
        id=f'{height}x{width}'
    )

def random_mf_stride( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    return pytest.param(
        rs1,
        rs2,
        stride_s1,
        stride_rd,
        id=f'{height}x{width}x{stride_s1}x{stride_rd}'
    )

def random_mf_x32( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs1 = (rs1 * np.iinfo(np.int8).max).astype(np.int32)
    rs2 = np.random.random((1, 1)).astype('float32')
    return pytest.param(
        rs1,
        rs2,
        id=f'{height}x{width}'
    )

def random_mf_stride_x32( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs1 = (rs1 * np.iinfo(np.int8).max).astype(np.int32)
    rs2 = np.random.random((1, 1)).astype('float32')
    return pytest.param(
        rs1,
        rs2,
        stride_s1,
        stride_rd,
        id=f'{height}x{width}x{stride_s1}x{stride_rd}'
    )

def random_mf_x8_hf( height, width ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    rs2 = rs2 * 128
    return pytest.param(
        rs1,
        rs2,
        id=f'{height}x{width}'
    )

def random_mf_stride_x8_hf( height, width, stride_s1, stride_rd ):
    rs1 = np.random.random((height, width)).astype('float16') * ( 1 - ( -1 ) ) + ( -1 )
    rs2 = np.random.random((1, 1)).astype('float32')
    rs2 = rs2 * 128
    return pytest.param(
        rs1,
        rs2,
        stride_s1,
        stride_rd,
        id=f'{height}x{width}x{stride_s1}x{stride_rd}'
    )

def random_m( dtype, width, height ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return pytest.param(
        rs1,
        id=f'{width}x{height}'
    )

def random_m_stride( dtype, width, height, sstride1 ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return pytest.param(
        rs1,
        sstride1,
        id=f'{width}x{height}x{sstride1}'
    )

def special_float_m( dtype, num, special_hex ):
    s1 = np.linspace( -1, 1, 256, dtype=dtype ).reshape( 16, 16 )
    sa = np.array( [special_hex], dtype=np.int16 )
    sa.dtype = dtype
    s1[num % 15][6] = sa[0]

    return pytest.param(
        s1,
        id=f'{num}x{special_hex}'
    )

def random_m_dim( dtype, width, height, dim ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return pytest.param(
        rs1,
        dim,
        id=f'{width}x{height}x{dim}'
    )

def random_m_stride_dim( dtype, width, height, sstride1, dim ):
    rs1 = np.random.normal( size = (height, width)).astype(dtype)
    return pytest.param(
        rs1,
        sstride1,
        dim,
        id=f'{width}x{height}x{sstride1}x{dim}'
    )

def special_float_m_dim( dtype, num, special_hex, dim ):
    s1 = np.linspace( -1, 1, 256, dtype=dtype ).reshape( 16, 16 )
    sa = np.array( [special_hex], dtype=np.int16 )
    sa.dtype = dtype
    s1[num % 15][6] = sa[0]

    return pytest.param(
        s1,
        dim,
        id=f'{num}x{special_hex}x{dim}'
    )

def ramdom_veemacc_mm_all_sum( height, width ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        id=f'{height}x{width}'
    )

def ramdom_veemacc_mm_all_sum_stride( height, width, stride_s1, stride_s2 ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        stride_s1,
        stride_s2,
        id=f'{height}x{width}x{stride_s1}x{stride_s2}'
    )

def ramdom_veemacc_mm( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        dim, 
        id=f'{height}x{width}x{dim}'
    )

def ramdom_veemacc_mm_stride( height, width, stride_s1, stride_s2, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        stride_s1,
        stride_s2,
        dim,
        id=f'{height}x{width}x{stride_s1}x{stride_s2}x{dim}'
    )

def ramdom_veemacc_mm_overlap( height, width, overlap_addr, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((height, width)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        overlap_addr,
        dim,
        id=f'{height}x{width}x{overlap_addr}x{dim}'
    )

def ramdom_veemacc_mv( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        dim,
        id=f'{height}x{width}x{dim}'
    )

def ramdom_veemacc_mv_stride( height, width, stride_s1, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        stride_s1,
        dim,
        id=f'{height}x{width}x{stride_s1}x{dim}'
    )

def ramdom_veemacc_mv_overlap( height, width, overlap_addr, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    if dim ==  1:
        rs2 = np.random.random((1, width)).astype('float16')
    else:
        rs2 = np.random.random((height, 1)).astype('float16')

    return pytest.param(
        rs1, 
        rs2,
        overlap_addr,
        dim,
        id=f'{height}x{width}x{dim}'
    )

def ramdom_veemacc_mf( height, width, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((1, 1)).astype('float32')

    return pytest.param(
        rs1, 
        rs2,
        dim,
        id=f'{height}x{width}x{dim}'
    )

def ramdom_veemacc_mf_stride( height, width, stride_s1, dim ):
    rs1 = np.random.random((height, width)).astype('float16')
    rs2 = np.random.random((1, 1)).astype('float32')

    return pytest.param(
        rs1, 
        rs2,
        stride_s1,
        dim,
        id=f'{height}x{width}x{stride_s1}x{dim}'
    )

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
    return pytest.param(
        rs1, 
        id = f'{height}x{width}'
    )

def metr_m( height, weight ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return pytest.param(
        rs,
        id = f'{height}x{weight}'
    )

def metr_m_stride( height, weight, stride_s, stride_d ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return pytest.param(
        rs,
        stride_s,
        stride_d,
        id = f'{height}x{weight}x{stride_s}x{stride_d}'
    )

def metr_m_misaligned_block( height, weight, off_s, off_d ):
    rs = np.random.random( ( height, weight ) ).astype( 'float16' ) * 2 - 1
    return pytest.param(
        rs,
        off_s,
        off_d,
        id = f'{height}x{weight}x{off_s}x{off_d}'
    )

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

def random_velkrelu_mv( height, width, vlen, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vlen ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return pytest.param( 
        rs1, 
        rs2,
        dim_flag,
        id = f'{height}x{width}x{vlen}x{dim_flag}'
    )

def random_velkrelu_special_mv( height, width, vlen, dim_flag ):
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

    return pytest.param( 
        rs1, 
        rs2,
        dim_flag,
        id = f'{height}x{width}x{vlen}x{dim_flag}'
    )

def random_velkrelu_stride_mv( height, width, vlen, stride_s, stride_d, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vlen ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return pytest.param( 
        rs1, 
        rs2,
        dim_flag,
        stride_s, 
        stride_d,
        id = f'{height}x{width}x{vlen}x{dim_flag}x{stride_s}x{stride_d}'
    )

def random_velkrelu_misaligned_mv( height, width, vlen, offset, dim_flag ):
    rs1 = np.random.normal( 0.0, 1.0, height*width ).astype( np.float16 ).reshape( height, width )
    rs2 = np.random.normal( 0.0, 1.0, vlen ).astype( np.float16 )
    if 1 == dim_flag:
        rs1 = rs1.swapaxes( 1, 0 )

    return pytest.param( 
        rs1, 
        rs2,
        dim_flag,
        offset,
        id = f'{height}x{width}x{vlen}x{dim_flag}x{offset}'
    )

def random_velut_m( width, height, tsize ):
    rs1 = np.random.randint( 29, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 30 ).astype( np.half )
    return pytest.param(
        rs1, 
        rs2,
        tsize,
        id = f'{width}x{height}x{tsize}'
    )

def random_velut_m_full_fill_l1b( width, height, tsize ):
    rs1 = np.random.randint( 64 * 1024 - 1, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 64 * 1024 ).astype( np.half )
    return pytest.param(
        rs1, 
        rs2,
        tsize,
        id = f'{width}x{height}x{tsize}'
    )

def random_velut_m_special( width, height, tsize ):
    # special float table   0,    -0,     inf,   -inf,    nan,    0.1,   10,    65500,  6.104e-05, 6.e-08
    rs1 = np.array( [0000, 0x8000, 0x7c00, 0xfc00, 0x7e00, 0x2e66, 0x4900, 0x7bff,  0x0400,    0x0001], dtype=np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace(-3.0, 3.0, 0xfc01).astype(np.half)
    return pytest.param(
        rs1, 
        rs2,
        tsize,
        id = f'{width}x{height}x{tsize}'
    )

def random_velut_m_stride( width, height, tsize, dstride, sstride ):
    rs1 = np.random.randint( 29, size = width * height ).astype(np.int16).reshape( height, width )
    rs1.dtype = np.half
    rs2 = np.linspace( -3.0, 3.0, 30 ).astype( np.half )
    return pytest.param(
        rs1, 
        rs2,
        tsize,
        dstride,
        sstride,
        id = f'{width}x{height}x{tsize}x{dstride}x{sstride}'
    )

def random_meconv_mm( h, w, cin, cout, kh, kw, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{padding}x{sk}x{dl}'
    )

def random_meconv_mm_stride( h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{stride_s1}x{stride_s2}x{stride_d}x{padding}x{sk}x{dl}'
    )

def random_meconv_mm_misaligned_block( h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = np.random.random(shape_input).astype('float16') * 2 - 1
    vs2 = np.random.random(shape_filter).astype('float16') * 2 - 1
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{off_s1}x{off_s2}x{off_d}x{padding}x{sk}x{dl}'
    )

def meconv_mm_special_fp( h, w, cin, cout, kh, kw, padding, sk, dl ):
    vs1 = np.array([0.0, -0.0, np.half('inf'), np.half('-inf'), np.half('nan'),
                    0.1, 10, 65500, 6.104e-05, 6.e-08], dtype=np.float16).reshape((1, 1, 10, 1))
    vs2 = np.array([0.0, -0.0, np.half('inf'), np.half('-inf'), np.half('nan'),
                    0.1, 10, 65500, 6.104e-05, 6.e-08], dtype=np.float16).reshape((1, 1, 1, 10))
    return pytest.param(
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{padding}x{sk}x{dl}'
    )

def random_meconv_x8_mm( h, w, cin, cout, kh, kw, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{padding}x{sk}x{dl}'
    )

def random_meconv_x8_mm_stride( h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{stride_s1}x{stride_s2}x{stride_d}x{padding}x{sk}x{dl}'
    )

def random_meconv_x8_mm_misaligned_block( h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl ):
    shape_input = [1, h, w, cin]
    shape_filter = [kh, kw, cin, cout]
    vs1 = (np.random.random(shape_input) * ( 256 ) - 128 ).astype('int8')
    vs2 = (np.random.random(shape_filter) * ( 256 ) - 128 ).astype('int8')
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{off_s1}x{off_s2}x{off_d}x{padding}x{sk}x{dl}'
    )

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
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{padding}x{sk}x{dl}'
    )

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
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{stride_s1}x{stride_s2}x{stride_d}x{padding}x{sk}x{dl}'
    )

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
    return pytest.param( 
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
        id=f'{h}x{w}x{cin}x{cout}x{kh}x{kw}x{off_s1}x{off_s2}x{off_d}x{padding}x{sk}x{dl}'
    )

def rvv_mask_generator(vlen):
    if vlen <= 8:
        return np.array([0xa], dtype=np.uint8)
    elif vlen > 8 and vlen <= 16:
        return np.array([0x5a5a], dtype=np.uint16)
    elif vlen > 16 and vlen <= 32:
        return np.array([0x5a55aa5a], dtype=np.uint32)
    else:
        return np.array([0x5a55aa5aff005faf], dtype=np.uint64)

def rvv_v_generator(vlen, dtype=np.int16):
    return np.linspace(1, 0xffff, vlen, dtype=dtype)

@pytest.fixture(scope='function', autouse=True)
def workdir(request, tmpdir_factory):
    test_name = request.function.__self__.__class__.__name__ + '.' + request.function.__name__

    request.cls.workdir = tmpdir_factory.mktemp(test_name)