import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.velkrelu_mv import *

class BaseCase_velkrelu_mv(BaseCase):
    header = '#include "velkrelu.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    footer = ''

class Case_base(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {dim} )'

class Case_inplace_src1(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_INPLACE_SRC1_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_INPLACE_SRC1_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {dim} )'

class Case_stride(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, stride_s, stride_d, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_STRIDED_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {stride_s}, {stride_d}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_STRIDED_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s}, {stride_d}, {dim} )'

class Case_misaligned_stride(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, stride_s, stride_d, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_MISALIGNED_STRIDE_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {stride_s}, {stride_d}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_MISALIGNED_STRIDE_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s}, {stride_d}, {dim} )'

class Case_misaligned_load(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, offset, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_MISALIGNED_LOAD_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {offset}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_MISALIGNED_LOAD_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {offset}, {dim} )'

class Case_misaligned_store(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rs1, rs2, dim, offset, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if 0 == dim:
            return f'TEST_VELKRELU_MV_MISALIGNED_STORE_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[1]}, {offset}, {dim} )'
        else:
            return f'TEST_VELKRELU_MV_MISALIGNED_STORE_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {offset}, {dim} )'


class Case_outof_limit(BaseCase_velkrelu_mv):
    def template( self, num, name, rd, rd_addr, src_addr, src2_addr, height, width, vlen, dim_flag ):
        return f'TEST_VELKRELU_MV_OUTOF_LIMIT( {num}, {rd_addr}, {src_addr}, {src2_addr}, {height}, {width}, {vlen}, {dim_flag} )'

class BaseTest_velkrelu_mv(BaseTest):

    @pytest.mark.parametrize( 'rs1, rs2, dim', [
        #************************************************************************/
        #*                    Sanity tests                                      */
        #************************************************************************/
        # Small case (2, 2) and (2)
        random_velkrelu_mv( 2, 2, 2, 0 ),
        random_velkrelu_mv( 2, 2, 2, 1 ),
        # Medium case (64, 64) and (64)
        random_velkrelu_mv( 64, 64, 64, 0 ),
        random_velkrelu_mv( 64, 64, 64, 1 ),
        # Large case (512, 512) and (512)
        random_velkrelu_mv( 512, 512, 512, 0 ),
        random_velkrelu_mv( 512, 512, 512, 1 ),

        #************************************************************************/
        #*                    Shape tests                                      */
        #************************************************************************/
        # Test dim = 1
        # (1, 1) and (1)
        random_velkrelu_mv( 1, 1, 1, 0 ),
        random_velkrelu_mv( 1, 1, 1, 1 ),

        # (1, 1024) and (1024)
        random_velkrelu_mv( 1, 1024, 1024, 0 ),
        random_velkrelu_mv( 1024, 1, 1024, 1 ),

        # (1024, 1) and (1)
        random_velkrelu_mv( 1024, 1, 1, 0 ),
        random_velkrelu_mv( 1, 1024, 1, 1 ),

        #ifdef FULL_TEST
        # Test large dim size, to almost fill L1B fully.
        # 638kB + 2kB + 638kB = 1278kB
        # (319, 1024) and (1024)
        random_velkrelu_mv( 319, 1024, 1024, 0 ),
        random_velkrelu_mv( 1024, 319, 1024, 1 ),
        #endif

        # Small normal shapes
        # (24, 27) and (27)
        random_velkrelu_mv( 24, 27, 27, 0 ),
        random_velkrelu_mv( 27, 24, 27, 1 ),
        # (52, 68) and (68)
        random_velkrelu_mv( 52, 68, 68, 0 ),
        random_velkrelu_mv( 68, 52, 68, 1 ),

        # Large normal shapes
        # (512, 256) and (256)
        random_velkrelu_mv( 512, 256, 256, 0 ),
        random_velkrelu_mv( 256, 512, 256, 1 ),

        # Test blocking edge cases
        # (20, 63) and (63)
        random_velkrelu_mv( 20, 63, 63, 0 ),
        random_velkrelu_mv( 63, 20, 63, 1 ),
        # (64, 65) and (65)
        random_velkrelu_mv( 64, 65, 65, 0 ),
        random_velkrelu_mv( 65, 64, 65, 1 ),
        # (64, 64) and (64)
        random_velkrelu_mv( 64, 64, 64, 0 ),
        random_velkrelu_mv( 64, 64, 64, 1 ),    
    ])
    def test_base( self, rs1, rs2, dim ):
        simulate( self, Case_base, rs1=rs1, rs2=rs2, dim=dim )

    @pytest.mark.parametrize( 'rs1, rs2, dim', [
        #************************************************************************/
        #*                    Computation in place tests                        */
        #************************************************************************/
        # dest == rs1
        random_velkrelu_mv( 5, 5, 5, 0),
        random_velkrelu_mv( 5, 5, 5, 1),
    ])
    def test_inplace_src1( self, rs1, rs2, dim ):
        simulate( self, Case_inplace_src1, rs1=rs1, rs2=rs2, dim=dim )

    @pytest.mark.parametrize( 'rs1, rs2, dim, stride_s, stride_d', [
        #************************************************************************/
        #*                    Stride tests                                      */
        #************************************************************************/
        # stride = width = 64
        random_velkrelu_stride_mv( 20, 32, 32, 64, 64, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 64, 64, 1 ),
        # Test src1/dest stride combinations
        # src1 width = 64, stride = 128
        random_velkrelu_stride_mv( 20, 32, 32, 128, 64, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 128, 64, 1 ),
        # dst width = 64, stride = 128
        random_velkrelu_stride_mv( 20, 32, 32, 64, 128, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 64, 128, 1 ),
        # src1 and dst are both strided
        random_velkrelu_stride_mv( 20, 32, 32, 64, 128, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 64, 128, 1 ),
        
        #dim=0, row=1, rs1 and rs2 all stride < width test
        random_velkrelu_stride_mv( 1, 32, 32, 11, 13, 0 ),
        #dim=1, row=1, rs1 and rs2 all stride < width test
        random_velkrelu_stride_mv( 1, 32, 1, 11, 13, 1 ),
    ] )
    def test_stride( self, rs1, rs2, dim, stride_s, stride_d ):
        simulate( self, Case_stride, rs1=rs1, rs2=rs2, dim=dim, stride_s=stride_s, stride_d=stride_d )

    @pytest.mark.parametrize( 'rs1, rs2, dim, stride_s, stride_d', [
        #************************************************************************/
        #*                    Misaligned stride tests                           */
        #************************************************************************/
        # The stride is not aligned with element of matrix is captured by misaligned
        # address exception.
        # stride_s is not aligned with element of matrix
        random_velkrelu_stride_mv( 20, 32, 32, 63, 128, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 63, 128, 1 ),
        # stride_d is not aligned with element of matrix
        random_velkrelu_stride_mv( 20, 32, 32, 64, 129, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 64, 129, 1 ),
        # stride_d less than width
        random_velkrelu_stride_mv( 20, 32, 32, 64, 60, 0 ),
        random_velkrelu_stride_mv( 20, 32, 20, 64, 60, 1 ),
    ] )
    def test_misaligned_stride( self, rs1, rs2, dim, stride_s, stride_d ):
        simulate( self, Case_misaligned_stride, rs1=rs1, rs2=rs2, dim=dim, stride_s=stride_s, stride_d=stride_d )

    #************************************************************************/
    #*                    Misaligned tests                                  */
    #************************************************************************/
    @pytest.mark.parametrize( 'rs1, rs2, dim, offset', [
        random_velkrelu_misaligned_mv( 10, 10, 10, 1, 1 ),
        random_velkrelu_misaligned_mv( 10, 10, 10, 1, 0 ),
    ])
    def test_misaligned_load( self, rs1, rs2, dim, offset ):
        simulate( self, Case_misaligned_load, rs1=rs1, rs2=rs2, dim=dim, offset=offset )

    @pytest.mark.parametrize( 'rs1, rs2, dim, offset', [
        random_velkrelu_misaligned_mv( 10, 10, 10, 1, 0 ),
        random_velkrelu_misaligned_mv( 10, 10, 10, 1, 1 ),
    ])
    def test_misaligned_store( self, rs1, rs2, dim, offset ):
        simulate( self, Case_misaligned_store, rs1=rs1, rs2=rs2, dim=dim, offset=offset )

    @pytest.mark.parametrize( 'rs1, rs2, dim', [
        #************************************************************************/
        #*                    Special float16 number tests                      */
        #************************************************************************/
        random_velkrelu_special_mv( 9, 9, 9, 0 ),
        random_velkrelu_special_mv( 9, 9, 9, 1 ),  
    ])
    def test_special( self, rs1, rs2, dim ):
        simulate( self, Case_base, rs1=rs1, rs2=rs2, dim=dim )

    # @pytest.mark.parametrize( 'rd_addr, src1_addr, src2_addr, height, width, vlen, dim_flag', [
    #     #************************************************************************/
    #     #*                    Test address are out of L1B or IMB                */
    #     #************************************************************************/
    #     #if SPIKE_EXCEPTION_BUG_FIXED
    #     # Starting address of rs1 is not in the L1B
    #     [ 'VELKRELU_RD_ADDR', 'NOT_L1B_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'NOT_L1B_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     # Starting address of rs2 is not in the L1B
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'NOT_L1B_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'NOT_L1B_ADDR', 20, 20, 20, 1 ],
    #     # Starting address of rd is not in the L1B
    #     [ 'NOT_L1B_ADDR', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'NOT_L1B_ADDR', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],

    #     # Starting address of rs1 is not in the IMB
    #     [ 'VELKRELU_RD_ADDR', 'NOT_IMB_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'NOT_IMB_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     # Starting address of rs2 is not in the L1B
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'NOT_IMB_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'NOT_IMB_ADDR', 20, 20, 20, 1 ],
    #     # Starting address of rd is not in the L1B
    #     [ 'NOT_IMB_ADDR', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'NOT_IMB_ADDR', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     # Ending address of rs1 is out of L1B
    #     [ 'VELKRELU_RD_ADDR', 'ALMOST_UPPER_L1B', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'ALMOST_UPPER_L1B', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     # Ending address of rs2 is out of L1B
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'ALMOST_UPPER_L1B', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'ALMOST_UPPER_L1B', 20, 20, 20, 1 ],
    #     # Ending address of rd is not in the L1B
    #     [ 'ALMOST_UPPER_L1B', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'ALMOST_UPPER_L1B', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],

    #     # Ending address of rs1 is out of IMB
    #     [ 'VELKRELU_RD_ADDR', 'ALMOST_UPPER_IMB', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'ALMOST_UPPER_L1B', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     # Ending address of rs2 is out of IMB
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'ALMOST_UPPER_IMB', 20, 20, 20, 0 ],
    #     [ 'VELKRELU_RD_ADDR', 'VELKRELU_RS1_ADDR', 'ALMOST_UPPER_IMB', 20, 20, 20, 1 ],
    #     # Ending address of rd is out of L1B
    #     [ 'ALMOST_UPPER_IMB', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 0 ],
    #     [ 'ALMOST_UPPER_IMB', 'VELKRELU_RS1_ADDR', 'VELKRELU_RS2_ADDR', 20, 20, 20, 1 ],
    #     #endif        
    # ] )
    # def test_outof_limit( self, rd_addr, src1_addr, src2_addr, height, width, vlen, dim_flag ):
    #     simulate( self, Case_outof_limit, rd_addr=rd_addr, src1_addr=src1_addr, src2_addr=src2_addr, height=height, width=width, vlen=vlen, dim_flag=dim_flag )

class Test_velkrelu_mv(BaseTest_velkrelu_mv):
    inst = Velkrelu_mv