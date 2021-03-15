import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.metr_m import *

class BaseCase_METR_M(BaseCase):
    head = '#include "metr.h"'

class Case_shape(BaseCase_METR_M):
    def template( self, num, name, rd, rs1, rs1_data, rs1_shape ):
        return f'TEST_METR( {num}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]} )'

class Case_stride(BaseCase_METR_M):
    def template( self, num, name, rd, rs1, stride_s, stride_d, rs1_data, rs1_shape ):
        return f'TEST_METR_STRIDE( {num}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s}, {stride_d} )'

class Case_misaligned_block(BaseCase_METR_M):
    def template( self, num, name, rd, rs1, off_s, off_d, rs1_data, rs1_shape ):
        return f'TEST_METR_MISALIGNED_BLOCK( {num}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]}, {off_s}, {off_d} )'

class Case_misaligned_base(BaseCase_METR_M):
    def template( self, num, name, rd, height, width, off_s, off_d ):
        return f'TEST_METR_EXCEPTION_MISALIGNED_BASE( {num}, {height}, {width}, {off_s}, {off_d} )'

class Case_misaligned_stride(BaseCase_METR_M):
    def template( self, num, name, rd, height, width, stride_s, stride_d ):
        return f'TEST_METR_EXCEPTION_MISALIGNED_STRIDE( {num}, {height}, {width}, {stride_s}, {stride_d} )'

class Case_invalid_param(BaseCase_METR_M):
    def template( self, num, name, rd, height, width ):
        return f'TEST_METR_EXCEPTION_INVALID_PARAM( {num}, {height}, {width} )'

class Case_access_fault(BaseCase_METR_M):
    def template( self, num, name, rd, height, width, s, d ):
        return f'TEST_METR_EXCEPTION_ACCESS_FAULT( {num}, {height}, {width}, {s}, {d} )'

class BaseTest_metr_m(BaseTest):

    @pytest.mark.parametrize( 'rs1', [
        #*****************************/
        #*      Sanity tests         */
        #*****************************/
        # Small case (4, 4) -> (4, 4)
        metr_m( 4, 4),
        # Medium case (64, 64) -> (64, 64)
        metr_m( 64, 64),
        # Large case (256, 256) -> (256, 256)
        metr_m( 256, 256),

        #*****************************/
        #*       Shape tests         */
        #*****************************/
        # Test dim=1
        # (1, 1) -> (1, 1)
        metr_m( 1, 1),
        # (1, 1024) -> (1024, 1)
        metr_m( 1, 1024),
        # (1024, 1) -> (1, 1024)
        metr_m( 1024, 1),

        #ifdef FULL_TEST
        # Test large dim size
        # (65535, 2)[256k] -> (2, 65535)[256k]
        metr_m( 65535, 2),
        # (2, 65535)[256k] -> (65535, 2)[256k]
        metr_m( 2, 65535),
        #endif

        # Small ordinary shapes
        # (7, 13) -> (13, 7)
        metr_m( 7, 13),
        # Medium ordinary shapes
        # (52, 73) -> (73, 52)
        metr_m( 52, 73),
        # Large ordinary shapes
        # (243, 322) -> (322, 243)
        metr_m( 243, 322),

        # Test blocking edge cases
        # (63, 65) -> (65, 63)
        metr_m( 63, 65),
        # (65, 63) -> (63, 65)
        metr_m( 65, 63),

    ] )
    def test_shape( self, rs1 ):
        simulate( self, Case_shape, rs1=rs1 )
    @pytest.mark.parametrize( 'rs1, stride_s, stride_d', [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == width == 128
        metr_m_stride( 64, 64, 128, 128),

        # Test src/dst stride combinations
        # src width = 128, stride = 256
        metr_m_stride( 64, 64, 256, 0),
        # dst width = 128, stride = 256
        metr_m_stride( 64, 64, 0, 256),
        # src and dst are both strided
        metr_m_stride( 64, 64, 256, 256),

        # Test misaligned strides
        metr_m_stride( 64, 64, 230, 154),
        # Test misaligned strides with ordinary shapes
        metr_m_stride( 51, 62, 314, 238),
        #rs1 row = 1, rs1 stride < width
        metr_m_stride( 1, 64, 19, 238),
        #rs1 cloumn = 1, rd stride < width
        metr_m_stride( 64, 1, 238, 19),
    ])
    def metr_m_stride( self, rs1, stride_s, stride_d ):
        simulate( self, Case_stride, rs1=rs1, stride_s=stride_s, stride_d=stride_d )

    @pytest.mark.parametrize( 'rs1, off_s, off_d', [
        #*****************************************/
        #*     Misaligned block address tests    */
        #*  (addresses are not 128-byte aligned) */
        #*****************************************/
        # Test misaligned src address
        metr_m_misaligned_block( 64, 64, 2, 0 ),
        # Test misaligned dst address
        metr_m_misaligned_block( 64, 64, 0, 2 ),
        # Test misaligned src/dst address
        metr_m_misaligned_block( 64, 64, 2, 2 ),
    ] )
    def metr_m_misaligned_block( self, rs1, off_s, off_d ):
        simulate( self, Case_misaligned_block, rs1=rs1, off_s=off_s, off_d=off_d )

    #*****************************/
    #*     Test exceptions       */
    #*****************************/
    @pytest.mark.parametrize('height, width, off_s, off_d', [
        # Test misaligned addresses
        #   RS misaligned
        [ 1, 1, 31, 0 ],
        #   RD misaligned
        [ 1, 1, 0, 55 ],
        #   RS/RD misaligned
        [ 1, 1, 73, 13 ],
    ])
    def test_misaligned_base( self, height, width, off_s, off_d ):
        simulate( self, Case_misaligned_base, height=height, width=width, off_s=off_s, off_d=off_d )

    @pytest.mark.parametrize('height, width, stride_s, stride_d', [
        # Test misaligned strides
        #   RS stride misaligned
        [ 2, 2, 59, 0 ],
        #   RD stride misaligned
        [ 2, 2, 0, 63 ],
        #   RS/RD stride misaligned
        [ 2, 2, 71, 15 ],
        #   RD stride < width
        [ 2, 8, 0, 2 ],
    ])
    def test_misaligned_stride( self, height, width, stride_s, stride_d ):
        simulate( self, Case_misaligned_stride, height=height, width=width, stride_s=stride_s, stride_d=stride_d )    

    @pytest.mark.parametrize('height, width', [
        # Test invalid parameter
        #   height == 0
        [ 0, 1 ],
        #   width == 0
        [ 1, 0 ],
        #   height == width == 0
        [ 0, 0 ],
    ])
    def test_invalid_param( self, height, width ):
        simulate( self, Case_invalid_param, height=height, width=width )  

    @pytest.mark.parametrize('height, width, s, d', [
        # Test access fault
        #   Invalid write to L1 buffer
        [ 1, 1, 'L1B_ADDR', 'L1B_ADDR+128' ],
        #   Write rd over IM buffer
        [ 2, 2, 'L1B_ADDR', 'IMB_END-2' ],
    ])
    def test_access_fault( self, height, width, s, d ):
        simulate( self, Case_access_fault, height=height, width=width, s=s, d=d )  

class Test_metr_m(BaseTest_metr_m):
    inst = Metr_m
