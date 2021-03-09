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


@pytest.fixture(scope='function', autouse=True)
def workdir(request, tmpdir_factory):
    test_name = request.function.__self__.__class__.__name__ + '.' + request.function.__name__

    request.cls.workdir = tmpdir_factory.mktemp(test_name)