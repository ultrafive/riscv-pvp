import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veadd_mv import *
from isa.custom.vesub_mv import *
from isa.custom.veemul_mv import *
from isa.custom.veemul_x32_mv import *
from isa.custom.vemax_mv import *
from isa.custom.vemin_mv import *

class BaseCase_vexxx_mv(BaseCase):
    header = '#include "vexxx_mv.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    foot = ''

class Case_basic_shape(BaseCase_vexxx_mv):
    def template( self, num, name, rd, rs1, vs2, dim_h, rs1_data, rs1_shape, vs2_data, vs2_shape ):
        if dim_h:
            return f'VEXXX_MV( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, 0 )'
        else:
            return f'VEXXX_MV( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[0]}, 1 )'

class Case_stride(BaseCase_vexxx_mv):
    def template( self, num, name, rd, rs1, vs2, dim_h, dstride, sstride1, rs1_data, rs1_shape, vs2_data, vs2_shape ):
        if dim_h:
            return f'VEXXX_MV_STRIDE( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, 0, {dstride}, {sstride1} )'
        else:
            return f'VEXXX_MV_STRIDE( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[0]}, 1, {dstride}, {sstride1} )'

class Case_inplace_rs1(BaseCase_vexxx_mv):
    def template( self, num, name, rd, rs1, vs2, dim_h, rs1_data, rs1_shape, vs2_data, vs2_shape ):
        if dim_h:
            return f'VEXXX_MV_INPLACE_RS1( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, 0 )'
        else:
            return f'VEXXX_MV_INPLACE_RS1( {num}, {name}, {rd}, {rs1_data}, {vs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[0]}, 1 )'

class Case_misaligned_base(BaseCase_vexxx_mv):
    def template( self, num, name, rd, width, height, dim, doff, soff1, soff2 ):
        return f'VEXXX_MV_MISALIGNED_BASE( {num}, {name}, {width}, {height}, {dim}, {doff}, {soff1}, {soff2})'

class Case_misaligned_stride(BaseCase_vexxx_mv):
    def template( self, num, name, rd, width, height, dim, dstride, sstride1 ):
        return f'VEXXX_MV_MISALIGNED_STRIDE( {num}, {name}, {width}, {height}, {dim}, {dstride}, {sstride1})'

class Case_invalid_param(BaseCase_vexxx_mv):
    def template( self, num, name, rd, width, height, dim ):
        return f'VEXXX_MV_INVALID_PARAM( {num}, {name}, {width}, {height}, {dim})'

class Case_access_fault(BaseCase_vexxx_mv):
    def template( self, num, name, rd, width, height, dim, result, val1, val2 ):
        return f'VEXXX_MV_ACCESS_FAULT( {num}, {name}, {width}, {height}, {dim}, {result}, {val1}, {val2})'

class BaseTest_vexxx_mv(BaseTest):

    @pytest.mark.parametrize('rs1, vs2, dim_h', [
        # Functional tests with basic data, dim_h
        linespace_mv( np.half, 64, 32, True ),
        linespace_mv( np.half, 64, 64, True ),
        linespace_mv( np.half, 128, 128, True ),
        linespace_mv( np.half, 256, 256, True ),
        linespace_mv( np.half, 256, 512, True ),

        # Functional tests with shapes, dim_h

        # near 64 mac
        linespace_mv( np.half, 63, 31, True ),
        linespace_mv( np.half, 65, 33, True ),
        linespace_mv( np.half, 63, 33, True ),

        # small shpaes
        linespace_mv( np.half, 1, 1, True ),
        linespace_mv( np.half, 10, 1, True ),
        linespace_mv( np.half, 1, 10, True ),
        linespace_mv( np.half, 10, 10, True ),

        # middel shape
        linespace_mv( np.half, 127, 127, True ),
        linespace_mv( np.half, 255, 127, True ),
        linespace_mv( np.half, 127, 255, True ),
        linespace_mv( np.half, 255, 255, True ),

        # full of l1buffer
        linespace_mv( np.half, 27306, 4, True ),
        linespace_mv( np.half, 426, 256, True ),
        linespace_mv( np.half, 256, 426, True ),

    ] )
    def test_basic_shapes_dimh( self, rs1, vs2, dim_h ):
        simulate( self, self.Case_basic_shape_inst, rs1=rs1, vs2=vs2, dim_h=dim_h )

    @pytest.mark.parametrize('rs1, vs2, dim_w',[
        # Functional tests with basic data, dim_w
        linespace_mv( np.half, 64, 32, False ),
        linespace_mv( np.half, 64, 64, False ),
        linespace_mv( np.half, 128, 128, False ),
        linespace_mv( np.half, 256, 256, False ),
        linespace_mv( np.half, 256, 512, False ),

        # Functional tests with shapes, dim_w

        # near 64 mac
        linespace_mv( np.half, 63, 31, False ),
        linespace_mv( np.half, 65, 33, False ),
        linespace_mv( np.half, 63, 33, False ),

        # small shapes
        linespace_mv( np.half, 1, 1, False ),
        linespace_mv( np.half, 10, 1, False ),
        linespace_mv( np.half, 1, 10, False ),
        linespace_mv( np.half, 10, 10, False ),

        # middle shape
        linespace_mv( np.half, 127, 127, False ),
        linespace_mv( np.half, 255, 127, False ),
        linespace_mv( np.half, 127, 255, False ),
        linespace_mv( np.half, 255, 255, False ),

        # full of l1buffer
        linespace_mv( np.half, 54613, 4, False ),
        linespace_mv( np.half, 853, 256, False ),
        linespace_mv( np.half, 256, 853, False ),

    ])
    def test_basic_shapes_dimw( self, rs1, vs2, dim_w ):
        simulate( self, self.Case_basic_shape_inst, rs1=rs1, vs2=vs2, dim_w=dim_w )

    @pytest.mark.parametrize('rs1, vs2, dim_h', [
        # functional tests with special float
        special_float_mv( np.half, 32, 1, True )
    ] )
    def test_special_float_dimh( self, rs1, vs2, dim_h ):
        simulate( self, self.Case_basic_shape_inst, rs1=rs1, vs2=vs2, dim_h=dim_h )

    @pytest.mark.parametrize('rs1, vs2, dim_w',[
        # functional tests with special float
        special_float_mv( np.half, 1, 32, False )

    ])
    def test_special_float_dimw( self, rs1, vs2, dim_w ):
        simulate( self, self.Case_basic_shape_inst, rs1=rs1, vs2=vs2, dim_w=dim_w )
    @pytest.mark.parametrize('rs1, vs2, dim_h, dstride, sstride1', [
        # Functional tests for stride

        linespace_mv_stride( np.half, 64, 32, True, 128, 0 ),
        linespace_mv_stride( np.half, 64, 32, True, 0, 128 ),
        linespace_mv_stride( np.half, 64, 32, True, 0, 0 ),
        linespace_mv_stride( np.half, 64, 32, True, 128, 128 ),

        linespace_mv_stride( np.half, 63, 31, True, 130, 130 ),
        linespace_mv_stride( np.half, 65, 33, True, 254, 254 ),
        linespace_mv_stride( np.half, 63, 33, True, 126, 126 ),

        linespace_mv_stride( np.half, 64, 32, False, 128, 0 ),
        linespace_mv_stride( np.half, 64, 32, False, 0, 128 ),
        linespace_mv_stride( np.half, 64, 32, False, 0, 0 ),
        linespace_mv_stride( np.half, 64, 32, False, 128, 128 ),

        linespace_mv_stride( np.half, 63, 31, False, 130, 130 ),
        linespace_mv_stride( np.half, 65, 33, False, 254, 254 ),
        linespace_mv_stride( np.half, 63, 33, False, 126, 126 ),

        # row=1, stride < width test
        linespace_mv_stride( np.half, 63, 1, False, 33, 33 ),
    ])
    def test_stride( self, rs1, vs2, dim_h, dstride, sstride1 ):
        simulate( self, self.Case_stride_inst, rs1=rs1, vs2=vs2, dim_h=dim_h, dstride=dstride, sstride1=sstride1 )
    '''
    @pytest.mark.parametrize('rs1, vs2, dim_h',[
        # Inplace compute tests for rd=rs1, rd=vs2, rs1=vs2, rd=rs1=vs2
        linespace_mv( np.half, 40, 40, True ),
        linespace_mv( np.half, 40, 40, False ),        
    ])
    def test_inplace_rs1( self, rs1, vs2, dim_h ):
        simulate( self, Case_inplace_rs1, rs1=rs1, vs2=vs2, dim_h=dim_h)
    '''

    @pytest.mark.parametrize( 'width, height, dim, doff, soff1, soff2', [
        # test exception with unaligned base adress

        # ==dimh
        # rd misaligned
        [ 2, 2, 0, 1, 0, 0 ],
        # rs1 misaligned
        [ 2, 2, 0, 0, 63, 0 ],
        # vs2 misaligned
        [ 2, 2, 0, 0, 0, 65 ],
        # rs1 + vs2 misaligned
        [ 2, 2, 0, 0, 127, 5 ],

        # ==dimw
        # rd misaligned
        [ 2, 2, 1, 1, 0, 0 ],
        # rs1 misaligned
        [ 2, 2, 1, 0, 63, 0],
        # vs2 misaligned
        [ 2, 2, 1, 0, 0, 65 ],
        # rs1 + vs2 misaligned
        [ 2, 2, 1, 0, 127, 5 ],
    ] )
    def test_misaligned_base( self, width, height, dim, doff, soff1, soff2 ):
        simulate( self, self.Case_misaligned_base_inst, width=width, height=height, dim=dim, doff=doff, soff1=soff1, soff2=soff2 )

    @pytest.mark.parametrize( 'width, height, dim', [
        # test exception with invalid param, width/height=0

        # === dim_h
        # width = 0
        [ 0, 2, 0 ],
        # height = 0
        [ 10, 0, 0 ],
        # height = 0
        [ 64, 0, 0 ],
        # width = 0, height = 0
        [ 0, 0, 0 ],

        # === dim_w
        # width = 0
        [ 0, 2, 1 ],
        # height = 0
        [ 10, 0, 1 ],
        # height = 0
        [ 64, 0, 1 ],
        # width = 0, height = 0
        [ 0, 0, 1 ],
    ] )
    def test_invalid_param( self, width, height, dim ):
        simulate( self, self.Case_invalid_param_inst, width=width, height=height, dim=dim )

    @pytest.mark.parametrize( 'width, height, dim, dstride, sstride1', [
        # test exception with unaligned stride

        # === dim_h
        # rd misaligned
        [ 2, 2, 0, 1, 0 ],
        # rd misaligned
        [ 2, 2, 0, 63, 0],
        # rs1 misaligned
        [ 2, 2, 0, 0, 65 ],
        # rs1 misaligned
        [ 2, 2, 0, 0, 127 ],

        # === dim_w
        # rd misaligned
        [ 2, 2, 1, 1, 0 ],
        # rd misaligned
        [ 2, 2, 1, 63, 0 ],
        # rs1 misaligned
        [ 2, 2, 1, 0, 65 ],
        # rs1 misaligned
        [ 2, 2, 1, 0, 127 ],
    ] )
    def test_misaligned_stride( self, width, height, dim, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, width=width, height=height, dim=dim, dstride=dstride, sstride1=sstride1 )

    @pytest.mark.parametrize( 'width, height, dim, result, val1, val2', [
        # test exception with access fault

        # ===dim_h
        # rd = 0, ddr
        [ 2, 2, 0, 0,           'RS1_ADDR', 'RS2_ADDR' ],
        # rd in ddr
        [ 2, 2, 0, 0x1000,      'RS1_ADDR', 'RS2_ADDR' ],
        # rd = L1B Base - 1
        [ 2, 2, 0, 0xbffffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = L1B Max + 1
        [ 2, 2, 0, 0xc0140000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Base - 1
        [ 2, 2, 0, 0xc03ffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Max + 1
        [ 2, 2, 0, 0xc0440000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd in llb
        [ 2, 2, 0, 0xf8001000,  'RS1_ADDR', 'RS2_ADDR'],

        # rs1 = 0, ddr
        [ 2, 2, 0, 'RD_ADDR', 0,           'RS2_ADDR'],
        # rs1 in ddr
        [ 2, 2, 0, 'RD_ADDR', 0x1000,      'RS2_ADDR'],
        # rs1 = L1B Base - 1
        [ 2, 2, 0, 'RD_ADDR', 0xbffffffc,  'RS2_ADDR'],
        # rs1 = L1B Max + 1
        [ 2, 2, 0, 'RD_ADDR', 0xc0140000,  'RS2_ADDR'],
        # rs1 = ImB Base - 1
        [ 2, 2, 0, 'RD_ADDR', 0xc03ffffc,  'RS2_ADDR'],
        # rs1 = ImB Max + 1
        [ 2, 2, 0, 'RD_ADDR', 0xc0440000,  'RS2_ADDR'],
        # rs1 in llb
        [ 2, 2, 0, 'RD_ADDR', 0xf8001000,  'RS2_ADDR'],

        # vs2 = 0, ddr
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0         ],
        # vs2 in ddr
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0x1000    ],
        # vs2 = L1B Base - 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xbffffffe],
        # vs2 = L1B Max + 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc0140000],
        # vs2 = ImB Base - 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc03ffffe],
        # vs2 = ImB Max + 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc0440000],
        # vs2 in llb
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xf8001000],

        # dim_w
        # rd = 0, ddr
        [ 2, 2, 1, 0,           'RS1_ADDR', 'RS2_ADDR'],
        # rd in ddr
        [ 2, 2, 1, 0x1000,      'RS1_ADDR', 'RS2_ADDR'],
        # rd = L1B Base - 1
        [ 2, 2, 1, 0xbffffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = L1B Max + 1
        [ 2, 2, 1, 0xc0140000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Base - 1
        [ 2, 2, 1, 0xc03ffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Max + 1
        [ 2, 2, 1, 0xc0440000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd in llb
        [ 2, 2, 1, 0xf8001000,  'RS1_ADDR', 'RS2_ADDR'],

        # rs1 = 0, ddr
        [ 2, 2, 1, 'RD_ADDR', 0,           'RS2_ADDR'],
        # rs1 in ddr
        [ 2, 2, 1, 'RD_ADDR', 0x1000,      'RS2_ADDR'],
        # rs1 = L1B Base - 1
        [ 2, 2, 1, 'RD_ADDR', 0xbffffffe,  'RS2_ADDR'],
        # rs1 = L1B Max + 1
        [ 2, 2, 1, 'RD_ADDR', 0xc0140000,  'RS2_ADDR'],
        # rs1 = ImB Base - 1
        [ 2, 2, 1, 'RD_ADDR', 0xc03ffffe,  'RS2_ADDR'],
        # rs1 = ImB Max + 1
        [ 2, 2, 1, 'RD_ADDR', 0xc0440000,  'RS2_ADDR'],
        # rs1 in llb
        [ 2, 2, 1, 'RD_ADDR', 0xf8001000,  'RS2_ADDR'],

        # vs2 = 0, ddr
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0         ],
        # vs2 in ddr
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0x1000    ],
        # vs2 = L1B Base - 1
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0xbffffffe],
        # vs2 = L1B Max + 1
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0xc0140000],
        # vs2 = ImB Base - 1
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0xc03ffffe],
        # vs2 = ImB Max + 1
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0xc0440000],
        # vs2 in llb
        [ 2, 2, 1, 'RD_ADDR', 'RS1_ADDR',  0xf8001000],
        
    ])
    def test_access_fault( self, width, height, dim, result, val1, val2 ):
        simulate( self, self.Case_access_fault_inst, width=width, height=height, dim=dim, result=result, val1=val1, val2=val2 )

class Test_veadd_mv(BaseTest_vexxx_mv):
    inst = Veadd_mv

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_basic_shape_inst(Case_basic_shape):
        pass
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_stride_inst(Case_stride):
        pass
class Test_vesub_mv(BaseTest_vexxx_mv):
    inst = Vesub_mv

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_basic_shape_inst(Case_basic_shape):
        pass
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_stride_inst(Case_stride):
        pass
class Test_veemul_mv(BaseTest_vexxx_mv):
    inst = Veemul_mv

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_basic_shape_inst(Case_basic_shape):
        pass
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_stride_inst(Case_stride):
        pass
class Test_veemul_x32_mv(BaseTest_vexxx_mv):
    inst = Veemul_x32_mv

    class Case_access_fault_inst(Case_access_fault):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_basic_shape_inst(Case_basic_shape):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        header = '#define X32_MV\n#include "vexxx_mv.h"'
    class Case_stride_inst(Case_stride):
        header = '#define X32_MV\n#include "vexxx_mv.h"'

    @pytest.mark.parametrize('rs1, vs2, dim_h', [
        # Functional tests with basic data, dim_h
        linespace_mv_x32( np.half, 64, 32, True ),
        linespace_mv_x32( np.half, 64, 64, True ),
        linespace_mv_x32( np.half, 128, 128, True ),
        linespace_mv_x32( np.half, 256, 256, True ),
        linespace_mv_x32( np.half, 256, 512, True ),

        # Functional tests with shapes, dim_h

        # near 64 mac
        linespace_mv_x32( np.half, 63, 31, True ),
        linespace_mv_x32( np.half, 65, 33, True ),
        linespace_mv_x32( np.half, 63, 33, True ),

        # small shpaes
        linespace_mv_x32( np.half, 1, 1, True ),
        linespace_mv_x32( np.half, 10, 1, True ),
        linespace_mv_x32( np.half, 1, 10, True ),
        linespace_mv_x32( np.half, 10, 10, True ),

        # middel shape
        linespace_mv_x32( np.half, 127, 127, True ),
        linespace_mv_x32( np.half, 255, 127, True ),
        linespace_mv_x32( np.half, 127, 255, True ),
        linespace_mv_x32( np.half, 255, 255, True ),

        # full of l1buffer
        linespace_mv_x32( np.half, 27306, 4, True ),
        linespace_mv_x32( np.half, 426, 256, True ),
        linespace_mv_x32( np.half, 256, 426, True ),
    ] )
    def test_basic_shapes_dimh( self, rs1, vs2, dim_h ):
        simulate( self, self.Case_basic_shape_inst, rs1=rs1, vs2=vs2, dim_h=dim_h )
    
    def test_basic_shapes_dimw( self ):
        pass

    @pytest.mark.parametrize('rs1, vs2, dim_h, dstride, sstride1', [
        # Functional tests for stride

        linespace_mv_stride_x32( np.half, 64, 32, True, 256, 0 ),
        linespace_mv_stride_x32( np.half, 64, 32, True, 0, 256 ),
        linespace_mv_stride_x32( np.half, 64, 32, True, 0, 0 ),
        linespace_mv_stride_x32( np.half, 64, 32, True, 256, 256 ),

        linespace_mv_stride_x32( np.half, 63, 31, True, 260, 260 ),
        linespace_mv_stride_x32( np.half, 65, 33, True, 508, 508 ),
        linespace_mv_stride_x32( np.half, 63, 33, True, 252, 252 ),

        # row=1, rs1 and rd stride < width test
        linespace_mv_stride_x32( np.half, 63, 1, True, 33, 33 ),
    ])
    def test_stride( self, rs1, vs2, dim_h, dstride, sstride1 ):
        simulate( self, self.Case_stride_inst, rs1=rs1, vs2=vs2, dim_h=dim_h, dstride=dstride, sstride1=sstride1 )

    @pytest.mark.parametrize( 'width, height, dim, doff, soff1, soff2', [
        # test exception with unaligned base adress

        # ==dimh
        # rd misaligned
        [ 2, 2, 0, 1, 0, 0 ],
        # rs1 misaligned
        [ 2, 2, 0, 0, 63, 0 ],
        # vs2 misaligned
        [ 2, 2, 0, 0, 0, 65 ],
        # rs1 + vs2 misaligned
        [ 2, 2, 0, 0, 127, 5 ],
    ] )
    def test_misaligned_base( self, width, height, dim, doff, soff1, soff2 ):
        simulate( self, self.Case_misaligned_base_inst, width=width, height=height, dim=dim, doff=doff, soff1=soff1, soff2=soff2 )

    @pytest.mark.parametrize( 'width, height, dim', [
        # test exception with invalid param, width/height=0

        # === dim_h
        # width = 0
        [ 0, 2, 0 ],
        # height = 0
        [ 10, 0, 0 ],
        # height = 0
        [ 64, 0, 0 ],
        # width = 0, height = 0
        [ 0, 0, 0 ],
    ] )
    def test_invalid_param( self, width, height, dim ):
        simulate( self, self.Case_invalid_param_inst, width=width, height=height, dim=dim )

    @pytest.mark.parametrize( 'width, height, dim, dstride, sstride1', [
        # test exception with unaligned stride

        # === dim_h
        # rd misaligned
        [ 2, 2, 0, 1, 0 ],
        # rd misaligned
        [ 2, 2, 0, 63, 0],
        # rs1 misaligned
        [ 2, 2, 0, 0, 65 ],
        # rs1 misaligned
        [ 2, 2, 0, 0, 127 ],
    ] )
    def test_misaligned_stride( self, width, height, dim, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, width=width, height=height, dim=dim, dstride=dstride, sstride1=sstride1 )

    @pytest.mark.parametrize( 'width, height, dim, result, val1, val2', [
        # test exception with access fault

        # ===dim_h
        # rd = 0, ddr
        [ 2, 2, 0, 0,           'RS1_ADDR', 'RS2_ADDR' ],
        # rd in ddr
        [ 2, 2, 0, 0x1000,      'RS1_ADDR', 'RS2_ADDR' ],
        # rd = L1B Base - 1
        [ 2, 2, 0, 0xbffffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = L1B Max + 1
        [ 2, 2, 0, 0xc0140000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Base - 1
        [ 2, 2, 0, 0xc03ffffe,  'RS1_ADDR', 'RS2_ADDR'],
        # rd = ImB Max + 1
        [ 2, 2, 0, 0xc0440000,  'RS1_ADDR', 'RS2_ADDR'],
        # rd in llb
        [ 2, 2, 0, 0xf8001000,  'RS1_ADDR', 'RS2_ADDR'],

        # rs1 = 0, ddr
        [ 2, 2, 0, 'RD_ADDR', 0,           'RS2_ADDR'],
        # rs1 in ddr
        [ 2, 2, 0, 'RD_ADDR', 0x1000,      'RS2_ADDR'],
        # rs1 = L1B Base - 1
        [ 2, 2, 0, 'RD_ADDR', 0xbffffffc,  'RS2_ADDR'],
        # rs1 = L1B Max + 1
        [ 2, 2, 0, 'RD_ADDR', 0xc0140000,  'RS2_ADDR'],
        # rs1 = ImB Base - 1
        [ 2, 2, 0, 'RD_ADDR', 0xc03ffffc,  'RS2_ADDR'],
        # rs1 = ImB Max + 1
        [ 2, 2, 0, 'RD_ADDR', 0xc0440000,  'RS2_ADDR'],
        # rs1 in llb
        [ 2, 2, 0, 'RD_ADDR', 0xf8001000,  'RS2_ADDR'],

        # vs2 = 0, ddr
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0         ],
        # vs2 in ddr
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0x1000    ],
        # vs2 = L1B Base - 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xbffffffe],
        # vs2 = L1B Max + 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc0140000],
        # vs2 = ImB Base - 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc03ffffe],
        # vs2 = ImB Max + 1
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xc0440000],
        # vs2 in llb
        [ 2, 2, 0, 'RD_ADDR', 'RS1_ADDR',  0xf8001000],
        
    ])
    def test_access_fault( self, width, height, dim, result, val1, val2 ):
        simulate( self, self.Case_access_fault_inst, width=width, height=height, dim=dim, result=result, val1=val1, val2=val2 )

    def test_special_float_dimh( self ):
        pass

    def test_special_float_dimw( self ):
        pass

class Test_vemax_mv(BaseTest_vexxx_mv):
    inst = Vemax_mv

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_basic_shape_inst(Case_basic_shape):
        pass
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_stride_inst(Case_stride):
        pass
    def test_special_float_dimh( self ):
        pass

    def test_special_float_dimw( self ):
        pass

class Test_vemin_mv(BaseTest_vexxx_mv):
    inst = Vemin_mv

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_basic_shape_inst(Case_basic_shape):
        pass
    class Case_inplace_rs1_inst(Case_inplace_rs1):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_stride_inst(Case_stride):
        pass
    def test_special_float_dimh( self ):
        pass

    def test_special_float_dimw( self ):
        pass