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

def random_memul_hf_x8_mm( l ):
    [ lb, ub, m, k, n] = l
    dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2 ]

def random_memul_hf_x8_mm_stride( l ):
    [ lb, ub, m, k, n, stride_s1, stride_s2, stride_d ] = l
    dequant = (np.random.random((1,)) * 2 - 1).astype('float32')
    vs1 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    vs2 = ( np.random.random((m, k)) * ( ub - lb ) + lb ).astype('int8')
    return [ dequant, vs1, vs2, stride_s1, stride_s2, stride_d ]    

@pytest.fixture(scope='function', autouse=True)
def workdir(request, tmpdir_factory):
    test_name = request.function.__self__.__class__.__name__ + '.' + request.function.__name__

    request.cls.workdir = tmpdir_factory.mktemp(test_name)