import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.velkrelu_mf import *

class BaseCase_velkrelu_mf(BaseCase):
    header = '#include "velkrelu.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    foot = ''

class Case_base(BaseCase_velkrelu_mf):
    def template( self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELKRELU_MF_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} )'

class Case_inplace_src1(BaseCase_velkrelu_mf):
    def template( self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELKRELU_MF_INPLACE_SRC1_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} )'


class Case_misaligned_load(BaseCase_velkrelu_mf):
    def template( self, num, name, rd, rs1, rs2, offset, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELKRELU_MF_MISALIGNED_LOAD_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {offset} )'

class Case_misaligned_store(BaseCase_velkrelu_mf):
    def template( self, num, name, rd, rs1, rs2, offset, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VELKRELU_MF_MISALIGNED_STORE_INTERNAL( {num}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {offset} )'


class BaseTest_velkrelu_mf(BaseTest):

    @pytest.mark.parametrize( 'rs1, rs2', [
        # Enable this macro definition when the inconsistent of special float16
        # are fixed.
        # #define SPECIAL_FP16_INCONSIS_FIXED
        ################################################################################
        # Functional tests with normal input
        ###############################################################################
        ## The elements of source matrix are random floating number,
        # the source floating argument is normal negative floating number.
        #
        [ np.random.normal(0.0, 2.0, 20).astype(np.float16).reshape(5, 4), 
        np.array([-0.7686], dtype=np.float32) ],
        ## The elements of source matrix are random floating number,
        # the source floating argument is normal positive floating number.
        ##
        [np.random.normal(0.0, 65504, 20*63).astype(np.float16).reshape(20, 63), 
        np.array([0.7686], dtype=np.float32) ],

        ################################################################################
        # Functional tests with boundary value
        ###############################################################################
        ## The elements of source matrix are random floating number,
        # the source floating argument is minimal float16.
        ##
        #ifdef SPECIAL_FP16_INCONSIS_FIXED
        #TEST_VELKRELU_MF(4, 64, 65)
        #endif
        ## The elements of source matrix are random floating number,
        # the source floating argument is maximal float16.
        ##
        [ np.random.normal(0.0, 65504, 10*64).astype(np.float16).reshape(10, 64), 
        np.array([65504.0], dtype=np.float32) ],
        #ifdef FULL_TEST
        ## Test full fill L1B.
        ##
        [ np.random.normal(0.0, 65504, 320*1024).astype(np.float16).reshape(320, 1024), 
        np.array([2.0], dtype=np.float32) ],
        ## The elements of source matrix are each kind of special value,
        # negative, zero, positive floating number, positive infinity,
        # nagative infinity, maximal float16, minmal float16.
        # the source floating argument is positive infinity.
        ##
        #endif
        #ifdef SPECIAL_FP16_INCONSIS_FIXED
        #TEST_VELKRELU_MF(7, 5, 2)
        #endif
        ## The elements of source matrix are each kind of special value,
        # negative, zero, positive floating number, positive infinity,
        # nagative infinity, maximal float16, minmal float16.
        # the source floating argument is negative infinity.
        ##
        #ifdef SPECIAL_FP16_INCONSIS_FIXED
        #TEST_VELKRELU_MF(8, 5, 2)
        #endif
        ## The elements of source matrix are each kind of special value,
        # negative, zero, positive floating number, positive infinity,
        # nagative infinity, maximal float16, minmal float16.
        # the source floating argument is zero.
        ##
        [ np.array([-1.5, 0.0, 1.0, 1.5, np.half('inf'), np.half('-inf'), 65504, 5.96e-8, -65504, -5.96e-8], dtype=np.float16).reshape(5, 2), 
        np.array([0.0], dtype=np.float32) ],
        ## The elements of source matrix are all zero,
        # the source floating argument is normal positive floating number.
        ##
        [ np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float16).reshape(2, 2), 
        np.array([2.2], dtype=np.float32) ],
        ## The elements of source matrix are all zero,
        # the source floating argument is zero.
        ##
        #ifdef SPECIAL_FP16_INCONSIS_FIXED
        [ np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float16).reshape(2, 2), 
        np.array([0.0], dtype=np.float32) ],
        ## The elements of source matrix are all zero,
        # the source floating argument is positive infinity.
        ##
        [ np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float16).reshape(2, 2),
        np.array([float('inf')], dtype=np.float32) ],
        ## The elements of source matrix are all zero,
        # the source floating argument is negative infinity.
        ##
        [ np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float16).reshape(2, 2), 
        np.array([float('-inf')], dtype=np.float32) ],
        #endif
        ## The elements of source matrix are all positive infinity,
        # the source floating argument is zero.
        ##
        [ np.array([np.half('inf'), np.half('inf'), np.half('inf'), np.half('inf')], dtype=np.float16).reshape(2, 2), 
        np.array([0.0], dtype=np.float32) ],
        ## The elements of source matrix are all positive infinity,
        # the source floating argument is positive infinity.
        ##
        [ np.array([np.half('inf'), np.half('inf'), np.half('inf'), np.half('inf')], dtype=np.float16).reshape(2, 2), 
        np.array([float('inf')], dtype=np.float32) ],
        ## The elements of source matrix are all positive infinity,
        # the source floating argument is nagative infinity.
        ##
        [ np.array([np.half('inf'), np.half('inf'), np.half('inf'), np.half('inf')], dtype=np.float16).reshape(2, 2), 
        np.array([float('-inf')], dtype=np.float32) ],
        ## The elements of source matrix are all positive infinity,
        # the source floating argument is nomal positive floating number.
        ##
        [ np.array([np.half('inf'), np.half('inf'), np.half('inf'), np.half('inf')], dtype=np.float16).reshape(2, 2), 
        np.array([2.2222], dtype=np.float32) ],
        ## The elements of source matrix are all negative infinity,
        # the source floating argument is normal positive floating number.
        ##
        [ np.array([np.half('-inf'), np.half('-inf'), np.half('-inf'), np.half('-inf')], dtype=np.float16).reshape(2, 2), 
        np.array([2.2222], dtype=np.float32) ],
        ## The elements of source matrix are all negative infinity,
        # the source floating argument is zero.
        ##
        [ np.array([np.half('-inf'), np.half('-inf'), np.half('-inf'), np.half('-inf')], dtype=np.float16).reshape(2, 2), 
        np.array([0], dtype=np.float32) ],
        ## The elements of source matrix are all negative infinity,
        # the source floating argument is positive infinity.
        ##
        [ np.array([np.half('-inf'), np.half('-inf'), np.half('-inf'), np.half('-inf')], dtype=np.float16).reshape(2, 2), 
        np.array([float('inf')], dtype=np.float32) ],
        ## The elements of source matrix are all negative infinity,
        # the source floating argument is native infinity.
        ##
        [ np.array([np.half('-inf'), np.half('-inf'), np.half('-inf'), np.half('-inf')], dtype=np.float16).reshape(2, 2), 
        np.array([float('-inf')], dtype=np.float32) ],
  
    ])
    def test_base( self, rs1, rs2 ):
        simulate( self, Case_base, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'rs1, rs2', [
        ################################################################################
        # Functional tests with compuation in place of the first source operand
        ###############################################################################
        [ np.array([-1.5, 0.0, 1.0, 1.5, 100, -100], dtype=np.float16).reshape(2, 3), 
        np.array([2.2], dtype=np.float32) ]
    ])
    def test_inplace_src1( self, rs1, rs2 ):
        simulate( self, Case_inplace_src1, rs1=rs1, rs2=rs2 )

    ##########################################################################
    ##                    Misaligned tests                                  ##
    ##########################################################################
    @pytest.mark.parametrize( 'rs1, rs2, offset', [
        [ np.array([-1.5, 0.0, 1.0, 1.5, 2.0, -2.5] , dtype=np.float16).reshape(3, 2), 
        np.array([2.2], dtype=np.float32), 1 ]
    ])
    def test_misaligned_load( self, rs1, rs2, offset ):
        simulate( self, Case_misaligned_load, rs1=rs1, rs2=rs2, offset=offset )

    @pytest.mark.parametrize( 'rs1, rs2, offset', [
        [ np.array([-1.5, 0.0, 1.0, 1.5, 2.0, -2.5] , dtype=np.float16).reshape(3, 2), 
        np.array([2.2], dtype=np.float32), 1 ]
    ])
    def test_misaligned_store( self, rs1, rs2, offset ):
        simulate( self, Case_misaligned_store, rs1=rs1, rs2=rs2, offset=offset )


class Test_velkrelu_mf(BaseTest_velkrelu_mf):
    inst = Velkrelu_mf