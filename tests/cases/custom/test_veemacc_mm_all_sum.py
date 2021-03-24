import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veemacc_mm_all_sum import *

class BaseCase_veemacc_mm_all_sum(BaseCase):
    header = '#include "veemacc.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    footer = ''

class Case_shape(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'VEEMACC_ALL_SUM( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, 0 ,0 )'

class Case_stride(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, rs1, rs2, stride_s1, stride_s2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'VEEMACC_ALL_SUM( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s1}, {stride_s2} )'

class Case_misaligned_base_addr(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, height, width, off_s1, off_s2 ):
        return f'VEEMACC_ALL_MISALIGNED_BASE_ADDR( {num}, {name}, {height}, {width}, {off_s1}, {off_s2} )'

class Case_misaligned_stride(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, height, width, stride_s1, stride_s2 ):
        return f'VEEMACC_ALL_MISALIGNED_STRIDE( {num}, {name}, {height}, {width}, {stride_s1}, {stride_s2} )'

class Case_invalid_param(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, height, width ):
        return f'TEST_VEEMACC_ALL_INVALID_PARAM( {num}, {name}, {height}, {width} )'

class Case_access_fault(BaseCase_veemacc_mm_all_sum):
    def template( self, num, name, rd, val1, val2, height, width ):
        return f'TEST_VEEMACC_ALL_ACCESS_FAULT( {num}, {name}, {val1}, {val2}, {height}, {width} )'

class BaseTest_veemacc_mm_all_sum(BaseTest):

    @pytest.mark.parametrize( 'rs1, rs2', [
        # Test shapes

        #small shapes, m(odd, odd)
        ramdom_veemacc_mm_all_sum( 1, 1),
        ramdom_veemacc_mm_all_sum( 1, 3),
        ramdom_veemacc_mm_all_sum( 3, 1),
        ramdom_veemacc_mm_all_sum( 3, 3),

        #m(even, even)
        ramdom_veemacc_mm_all_sum( 2, 10),
        ramdom_veemacc_mm_all_sum( 10, 2),
        ramdom_veemacc_mm_all_sum( 2, 2),
        ramdom_veemacc_mm_all_sum( 10, 10),

        #m(odd, even), m(even ,odd)
        ramdom_veemacc_mm_all_sum( 19, 28),
        ramdom_veemacc_mm_all_sum( 28, 19),

        #64 MAC Engine boundary
        ramdom_veemacc_mm_all_sum( 31, 63),
        ramdom_veemacc_mm_all_sum( 32, 64),
        ramdom_veemacc_mm_all_sum( 33, 65),

        #middle shapes
        ramdom_veemacc_mm_all_sum( 35, 129),
        ramdom_veemacc_mm_all_sum( 36, 257),
        ramdom_veemacc_mm_all_sum( 131, 38),
        ramdom_veemacc_mm_all_sum( 258, 260),

        #full of L1 buffer
        #ramdom_veemacc_mm_all_sum( 54613, 4),
        ramdom_veemacc_mm_all_sum( 256, 853),
        ramdom_veemacc_mm_all_sum( 853, 256),

    ] )
    def test_shape( self, rs1, rs2 ):
        simulate( self, Case_shape, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'rs1, rs2, stride_s1, stride_s2', [
        #Test  stride,  stride >= ESIZE*width

        ramdom_veemacc_mm_all_sum_stride( 15, 15, 30, 30),
        ramdom_veemacc_mm_all_sum_stride( 15, 15, 30, 0),
        ramdom_veemacc_mm_all_sum_stride( 15, 15, 0, 30),

        ramdom_veemacc_mm_all_sum_stride( 15, 15, 0, 92),
        ramdom_veemacc_mm_all_sum_stride( 15, 15, 92, 0),
        ramdom_veemacc_mm_all_sum_stride( 15, 15, 92, 92),
        ramdom_veemacc_mm_all_sum_stride( 15, 15, 80, 68),

        ramdom_veemacc_mm_all_sum_stride( 34, 34, 130, 0),
        ramdom_veemacc_mm_all_sum_stride( 34, 34, 0, 130),
        ramdom_veemacc_mm_all_sum_stride( 34, 34, 130, 130),

        ramdom_veemacc_mm_all_sum_stride( 34, 34, 150, 0),
        ramdom_veemacc_mm_all_sum_stride( 34, 34, 210, 0),
        ramdom_veemacc_mm_all_sum_stride( 34, 34, 262, 130),
        ramdom_veemacc_mm_all_sum_stride( 34, 34, 262, 512),

        #row=1, rs and rd all stride < width test
        ramdom_veemacc_mm_all_sum_stride( 1, 15, 7, 7),
    ] )
    def test_stride( self, rs1, rs2, stride_s1, stride_s2 ):
        simulate( self, Case_stride, rs1=rs1, rs2=rs2, stride_s1=stride_s1, stride_s2=stride_s2 )

    @pytest.mark.parametrize( 'height, width, off_s1, off_s2', [
        #Exception test with misaligned base addr

        #rs1 misaligned
        [ 31, 32, 1, 0],
        #rs2 misaligned
        [ 31, 32, 0, 1],
        #rd and rs2 misaligned
        [ 31, 32, 1, 1],
        #rs1 misaligned
        [ 31, 32, 9, 0],
        #rs2 misaligned
        [ 31, 32, 0, 9],
        #rs1 and rs2 misaligned
        [ 31, 32, 9, 9],
    ] )
    def test_misaligned_base_addr( self, height, width, off_s1, off_s2 ):
        simulate( self, Case_misaligned_base_addr, height=height, width=width, off_s1=off_s1, off_s2=off_s2 )

    @pytest.mark.parametrize( 'height, width, stride_s1, stride_s2', [

        #Exception test with misaligned stride

        [ 32, 32, 67, 0],
        [ 32, 32, 0, 67],
        [ 32, 32, 67, 67],
    ] )
    def test_misaligned_stride( self, height, width, stride_s1, stride_s2 ):
        simulate( self, Case_misaligned_stride, height=height, width=width, stride_s1=stride_s1, stride_s2=stride_s2 )

    @pytest.mark.parametrize( 'height, width', [

        #Exception test with invalid params

        #height=0
        [ 0, 32],
        #width=0
        [ 32, 0],
        #height=width=0
        [ 0, 0],
    ] )
    def test_invalid_param( self, height, width ):
        simulate( self, Case_invalid_param, height=height, width=width )

    @pytest.mark.parametrize( 'val1, val2, height, width', [

        # Exception test with access fault

        #rs1 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0x400, 'VEADD_RS2_ADDR', 24, 24],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 0xbffffffc, 'VEADD_RS2_ADDR',  32, 32],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 0xc013fffc, 'VEADD_RS2_ADDR', 12, 24],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 0xc03ffffc, 'VEADD_RS2_ADDR', 32, 32],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0xc043fffc, 'VEADD_RS2_ADDR', 32, 32],


        #rs2 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RS1_ADDR', 0x400, 24, 24],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VEADD_RS1_ADDR', 0xbffffffc,  32, 32],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VEADD_RS1_ADDR', 0xc013fffc, 12, 24],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VEADD_RS1_ADDR', 0xc03ffffc, 32, 32],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RS1_ADDR', 0xc043fffc, 32, 32],
    ] )
    def test_access_fault( self, val1, val2, height, width ):
        simulate( self, Case_access_fault, val1=val1, val2=val2, height=height, width=width )


class Test_veemacc_mm_all_sum(BaseTest_veemacc_mm_all_sum):
    inst = Veemacc_mm_all_sum