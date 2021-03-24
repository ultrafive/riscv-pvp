import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.velut_m import *

class BaseCase_velut_m(BaseCase):
    header = '#include "velut_m.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    footer = ''

class Case_base(BaseCase_velut_m):
    def template( self, num, name, rd, rs1, rs2, tsize, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELUT_M_INTERNAL( {num}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs2_data}, {tsize}, 16, EQM )'

class Case_stride(BaseCase_velut_m):
    def template( self, num, name, rd, rs1, rs2, tsize, dstride, sstride, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELUT_M_STRIDE_INTERNAL( {num}, velut.m, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs2_data}, {tsize}, {dstride}, {sstride} )'

class Case_inplace_rs1(BaseCase_velut_m):
    def template( self, num, name, rd, rs1, rs2, tsize, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELUT_M_INPLACE_RS1_INTERNAL( {num}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs2_data}, {tsize} )'

class Case_misaligned_base(BaseCase_velut_m):
    def template( self, num, name, rd, width, height, doff, soff1, soff2  ):
        return f'TEST_VELUT_M_MISALIGNED_BASE( {num}, {width}, {height}, {doff}, {soff1}, {soff2} )'

class Case_invalid_param(BaseCase_velut_m):
    def template( self, num, name, rd, width, height ):
        return f'TEST_VELUT_M_INVALID_PARAM( {num}, {width}, {height} )'

class Case_misaligned_stride(BaseCase_velut_m):
    def template( self, num, name, rd, width, height, dstride, sstride ):
        return f'TEST_VELUT_M_MISALIGNED_STRIDE( {num}, {width}, {height}, {dstride}, {sstride} )'

class Case_access_fault(BaseCase_velut_m):
    def template( self, num, name, rd, width, height, dst, src1, src2 ):
        return f'TEST_VELUT_M_ACCESS_FAULT( {num}, {width}, {height}, {dst}, {src1}, {src2} )'

class BaseTest_velut_m(BaseTest):
    @pytest.mark.parametrize( 'rs1, rs2, tsize', [
        #*******************************************************************************
        # Functional tests with basic data
        #*****************************************************************************/
       random_velut_m( 32, 64, 30 ),
       random_velut_m( 64, 64, 30 ),
       random_velut_m( 128, 128, 30 ),
       random_velut_m( 224, 224, 30 ),
       random_velut_m( 256, 512, 30 ),

        #*******************************************************************************
        # Functional tests with shapes
        #*****************************************************************************/

        # near 64 column
       random_velut_m( 63, 31, 30 ),
       random_velut_m( 65, 33, 30 ),
       random_velut_m( 63, 64, 30 ),

        # small shapes
       random_velut_m( 1, 1, 30 ),
       random_velut_m( 20, 1, 30 ),
       random_velut_m( 1, 20, 30 ),
       random_velut_m( 20, 20, 30 ),

        # middle shape
       random_velut_m( 127, 127, 30 ),
       random_velut_m( 255, 127, 30 ),
       random_velut_m( 127, 255, 30 ),
       random_velut_m( 255, 255, 30 ),

        #ifdef FULL_TEST
        # full of l1buffer
       random_velut_m_full_fill_l1b( 288, 1024, 64*1024),
       random_velut_m_full_fill_l1b( 1024, 288, 64*1024),
        #endif
    ] )
    def test_base( self, rs1, rs2, tsize ):
        simulate( self, Case_base, rs1=rs1, rs2=rs2, tsize=tsize )

    @pytest.mark.parametrize( 'rs1, rs2, tsize', [
        #*******************************************************************************
        # Functional tests with special float
        #*****************************************************************************/
        random_velut_m_special( 5, 2, 64*1024 )
    ] )
    def test_special_float( self, rs1, rs2, tsize ):
        simulate( self, Case_base, rs1=rs1, rs2=rs2, tsize=tsize )

    @pytest.mark.parametrize( 'rs1, rs2, tsize, dstride, sstride', [
        #*******************************************************************************
        # Functional tests for stride
        #*****************************************************************************/
       random_velut_m_stride( 64, 26, 30, 128, 0 ),
       random_velut_m_stride( 64, 26, 30, 256, 0 ),
       random_velut_m_stride( 64, 26, 30, 0, 128 ),
       random_velut_m_stride( 64, 26, 30, 0, 256 ),
       random_velut_m_stride( 64, 26, 30, 128, 128 ),
       random_velut_m_stride( 64, 26, 30, 256, 256 ),
       random_velut_m_stride( 63, 26, 30, 130, 130 ),
       random_velut_m_stride( 65, 26, 30, 224, 224 ),
       random_velut_m_stride( 63, 26, 30, 126, 126 ),
        #row=1, rs1 and rd stride < width test
       random_velut_m_stride( 63, 1, 30, 17, 19 ),
    ] )
    def test_stride( self, rs1, rs2, tsize, dstride, sstride ):
        simulate( self, Case_stride, rs1=rs1, rs2=rs2, tsize=tsize, dstride=dstride, sstride=sstride )

    @pytest.mark.parametrize( 'rs1, rs2, tsize', [
        #*******************************************************************************
        # Inplace compute tests for rd=rs1, rd=rs2, rs1=rs2, rd=rs1=rs2
        #*****************************************************************************/
        # # rd = rs1
        random_velut_m( 4, 4, 30 )
    ])
    def test_inplace_rs1( self, rs1, rs2, tsize ):
        simulate( self, Case_inplace_rs1, rs1=rs1, rs2=rs2, tsize=tsize )

    @pytest.mark.parametrize( 'width, height, doff, soff1, soff2', [
        #*******************************************************************************
        # Test execption with unaligned base address
        #*****************************************************************************/
        # rd misaligned
        [ 2, 2, 1, 0, 0 ],
        # rs1 misaligned
        [ 2, 2, 0, 63, 0 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 0, 11, 5 ],
    ])
    def test_misaligned_base( self, width, height, doff, soff1, soff2 ):
        simulate( self, Case_misaligned_base, width=width, height=height, doff=doff, soff1=soff1, soff2=soff2 )

    @pytest.mark.parametrize( 'width, height', [
        #*******************************************************************************
        # Test execption with invalid param, width/height=0
        #*****************************************************************************/
        # width = 0
        [ 0, 2 ],
        # height = 0
        [ 10, 0 ],
        # height = 0
        [ 64, 0 ],
        # width = 0, height = 0
        [ 0, 0 ],
    ])
    def test_invalid_param( self, width, height ):
        simulate( self, Case_invalid_param, width=width, height=height )

    @pytest.mark.parametrize( 'width, height, dstride, sstride', [
        #*******************************************************************************
        # Test execption with unaligned stride
        #*****************************************************************************/
        # rd misaligned
        [ 2, 2, 3,  8 ],
        # rs1 misaligned
        [ 2, 2, 8, 5 ],
        # rd + rs1 misaligned
        [ 2, 2, 7, 9 ],
    ])
    def test_misaligned_stride( self, width, height, dstride, sstride ):
        simulate( self, Case_misaligned_stride, width=width, height=height, dstride=dstride, sstride=sstride )

    @pytest.mark.parametrize( 'width, height, dst, src1, src2', [
        #*******************************************************************************
        # Test execption with access fault
        #*****************************************************************************/
        # rd = 0, ddr
        [ 2, 2, 0,            'RS1_ADDR',  'RS2_ADDR' ],
        # rd = L1B Base - 1
        [ 2, 2, 0xbffffffe,   'RS1_ADDR',  'RS2_ADDR' ],
        # rd = L1B Max + 1
        [ 2, 2, 0xc0140000,   'RS1_ADDR',  'RS2_ADDR' ],
        # rd = ImB Base - 1
        [ 2, 2, 0xc03ffffe,   'RS1_ADDR',  'RS2_ADDR' ],
        # rd = ImB Max + 1
        [ 2, 2, 0xc0440000,   'RS1_ADDR',  'RS2_ADDR' ],
        # rd in llb
        [ 2, 2, 0xf8001000,   'RS1_ADDR',  'RS2_ADDR' ],
        # rs1 = 0, ddr
        [ 2, 2,  'RD_ADDR', 0,            'RS2_ADDR' ],
        # rs1 in ddr
        [ 2, 2,  'RD_ADDR', 0x1000,       'RS2_ADDR' ],
        # rs1 = L1B Base - 1
        [ 2, 2,  'RD_ADDR', 0xbffffffe,   'RS2_ADDR' ],
        # rs1 = L1B Max + 1
        [ 2, 2,  'RD_ADDR', 0xc0140000,   'RS2_ADDR' ],
        # rs1 = ImB Base - 1
        [ 2, 2,  'RD_ADDR', 0xc03ffffe,   'RS2_ADDR' ],
        # rs1 = ImB Max + 1
        [ 2, 2,  'RD_ADDR', 0xc0440000,   'RS2_ADDR' ],
        # rs1 in llb
        [ 2, 2,  'RD_ADDR', 0xf8001000,   'RS2_ADDR' ],

        # rs2 = 0, ddr
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0          ],
        # rs2 in ddr
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0x1000     ],
        # rs2 = L1B Base - 1
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0xbffffffe ],
        # rs2 = L1B Max + 1
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0xc0140000 ],
        # rs2 = ImB Base - 1
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0xc03ffffe ],
        # rs2 = ImB Max + 1
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0xc0440000 ],
        # rs2 in llb
        [ 2, 2,  'RD_ADDR',  'RS1_ADDR',  0xf8001000 ],
    ])
    def test_access_fault( self, width, height, dst, src1, src2 ):
        simulate( self, Case_access_fault, width=width, height=height, dst=dst, src1=src1, src2=src2 )    

class Test_velut_m(BaseTest_velut_m):
    inst = Velut_m