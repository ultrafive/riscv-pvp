import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.memul_mm import *
from isa.custom.memul_ts_mm import *
from isa.custom.memul_x8_mm import *
from isa.custom.memul_hf_x8_mm import *

class BaseCase_METMUL_MM(BaseCase):
    header = '#include "memul.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    foot = ''


class Case_base(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]} )'
class Case_stride(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, stride_s1, stride_s2, stride_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL_STRIDE( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {stride_s1}, {stride_s2}, {stride_d} )'

class Case_misaligned_block(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, off_s1, off_s2, off_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL_MISALIGNED_BLOCK( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {off_s1}, {off_s2}, {off_d} )'


def pytest_generate_tests(metafunc):
    # called once per each test function
    lb = metafunc.cls.lb
    ub = metafunc.cls.ub
    data_function = metafunc.cls.data_function[ metafunc.function.__name__ ]
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ data_function( [ lb, ub ] + param )  for param in params ]
    )


class BaseTest_memul_mm(BaseTest):
    params_base = [
        #*****************************/
        #*      Sanity tests         */
        #*****************************/
        # Small case (4, 4) x (4, 4)
        [ 4, 4, 4 ],
        # Medium case (64, 64) x (64, 64)
        [ 64, 64, 64 ],
        # Large case (256, 256) x (256, 256)
        [ 256, 256, 256 ],

        #*****************************/
        #*       Shape tests         */
        #*****************************/
        # Test dim=1
        # (1, 1) x (1, 1)
        [ 1, 1, 1 ],
        # (1, 1) x (1, 1024)
        [ 1, 1, 1024 ],
        # (1, 1024) x (1024, 1)
        [ 1, 1024, 1 ],
        # (1024, 1) x (1, 1)
        [ 1024, 1, 1 ],
        # (256, 256) x (256, 1)
        [ 256, 256, 1 ],
        # (256, 1) x (1, 256)
        [ 256, 1, 256 ],
        # (1, 256) x (256, 256)
        [ 1, 256, 256 ],

        # Test large dim size
        # (65535, 4)[512k] x (4, 2) = (65535, 2)[256k]
        [ 65535, 4, 2 ],
        # (128, 2048)[512k] x (2048, 128)[512k] = (128, 128)
        [ 128, 2048, 128 ],
        # (2, 4) x (4, 65535)[512k] = (2, 65535)[256k]
        [ 2, 4, 65535 ],

        # Small ordinary shapes
        # (7, 13) x (13, 9)
        [ 7, 13, 9 ],
        # Medium ordinary shapes
        # (52, 73) x (73, 42)
        [ 52, 73, 42 ],
        # Large ordinary shapes
        # (243, 322) x (322, 157)
        [ 243, 322, 157 ],

        # Test blocking edge cases
        [ 63, 65, 65 ],
        [ 65, 63, 65 ],
        [ 65, 65, 63 ],
        [ 63, 63, 65 ],
        [ 63, 65, 63 ],
        [ 65, 63, 63 ],
        [ 65, 65, 65 ],

        ]
    params_stride = [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == width == 128
        [ 64, 64, 64, 128, 128, 128 ],

        # Test src1/src2/dst stride combinations
        # src1 width = 128, stride = 256
        [ 64, 64, 64, 256, 0, 0 ],
        # src2 width = 128, stride = 256
        [ 64, 64, 64, 0, 256, 0 ],
        # dst width = 128, stride = 256
        [ 64, 64, 64, 0, 0, 256 ],
        # src1 and src2 are both strided
        [ 64, 64, 64, 256, 256, 0 ],
        # src1 and dst are both strided
        [ 64, 64, 64, 256, 0, 256 ],
        # src2 and dst are both strided
        [ 64, 64, 64, 0, 256, 256 ],
        # src1, src2 and dst are all strided
        [ 64, 64, 64, 256, 256, 256 ],

        # Test misaligned strides
        [ 64, 64, 64, 230, 154, 522 ],
        # Test misaligned strides with ordinary shapes
        [ 51, 62, 73, 314, 238, 452 ],

        #rs1 row=1, rs1 and rd stride < width test
        [ 1, 64, 64, 17, 0, 17 ],
        #rs2 row=1, rs2 stride < width test
        [ 64, 1, 64, 0, 31, 0 ],
    ]
    params_misaligned_block = [
        #*****************************************/
        #*     Misaligned block address tests    */
        #*  (addresses are not 128-byte aligned) */
        #*****************************************/
        # Test misaligned RS1 address
        [ 64, 64, 64, 2, 0, 0 ],
        # Test misaligned RS2 address
        [ 64, 64, 64, 0, 2, 0 ],
        # Test misaligned RD address
        [ 64, 64, 64, 0, 0, 2 ],
        # Test misaligned RS1/RS2/RD addresses
        [ 64, 64, 64, 18, 28, 8 ],
    ]
    params_softfloat = [
        #*****************************/
        #*   Special FP value tests  */
        #*****************************/
        # Test (+inf, -inf, 0, nan)T * (+inf, -inf, 0, nan)
        [ 4, 1, 4 ],
    ]
    params = { 'test_base': params_base, 'test_stride': params_stride, 'test_misaligned_block': params_misaligned_block,
    'test_softfloat_base': params_softfloat }
    def test_base( self, vs1, vs2 ):
        simulate( self, self.Case_base_inst, vs1=vs1, vs2=vs2 )

    def test_stride( self, vs1, vs2, stride_s1, stride_s2, stride_d ):
        simulate( self, self.Case_stride_inst, vs1=vs1, vs2=vs2, stride_s1=stride_s1, stride_s2=stride_s2, stride_d=stride_d )
    
    def test_misaligned_block( self, vs1, vs2, off_s1, off_s2, off_d ):
        simulate( self, self.Case_misaligned_block_inst, vs1=vs1, vs2=vs2, off_s1=off_s1, off_s2=off_s2, off_d=off_d )

    def test_softfloat_base( self, vs1, vs2 ):
        simulate( self, self.Case_base_inst, vs1=vs1, vs2=vs2 )

class Test_memul_mm(BaseTest_memul_mm):
    inst = Memul_mm

    lb = -1
    ub =  1
    data_function = { 'test_base':random_memul_mm, 'test_stride':random_memul_mm_stride, 'test_misaligned_block':random_memul_mm_misaligned_block, 'test_softfloat_base':softfloat_memul_mm  }
    argnames = { 'test_base':[ 'vs1', 'vs2' ], 'test_stride':[ 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ], 'test_misaligned_block':[ 'vs1', 'vs2', 'off_s1', 'off_s2', 'off_d' ], 'test_softfloat_base':[ 'vs1', 'vs2' ] }

    class Case_base_inst(Case_base):
        header = '#define HF\n#include "memul.h"'
    class Case_stride_inst(Case_stride):
        header = '#define HF\n#include "memul.h"'
    class Case_misaligned_block_inst(Case_misaligned_block):
        header = '#define HF\n#include "memul.h"'

class Test_memul_ts_mm(BaseTest_memul_mm):
    inst = Memul_ts_mm

    params_stride = [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == width == 128
        [ 64, 64, 64, 128, 128, 128 ],

        # Test src1/src2/dst stride combinations
        # src1 width = 128, stride = 256
        [ 64, 64, 64, 256, 0, 0 ],
        # src2 width = 128, stride = 256
        [ 64, 64, 64, 0, 256, 0 ],
        # dst width = 128, stride = 256
        [ 64, 64, 64, 0, 0, 256 ],
        # src1 and src2 are both strided
        [ 64, 64, 64, 256, 256, 0 ],
        # src1 and dst are both strided
        [ 64, 64, 64, 256, 0, 256 ],
        # src2 and dst are both strided
        [ 64, 64, 64, 0, 256, 256 ],
        # src1, src2 and dst are all strided
        [ 64, 64, 64, 256, 256, 256 ],

        # Test misaligned strides
        [ 64, 64, 64, 230, 154, 522 ],
        # Test misaligned strides with ordinary shapes
        [ 51, 62, 73, 314, 238, 452 ],
    ]
    params = { 'test_base': BaseTest_memul_mm.params_base, 'test_stride': params_stride, 'test_misaligned_block': BaseTest_memul_mm.params_misaligned_block,
    'test_softfloat_base': BaseTest_memul_mm.params_softfloat }  
    lb = -1
    ub =  1
    data_function = { 'test_base':random_memul_ts_mm, 'test_stride':random_memul_ts_mm_stride, 'test_misaligned_block':random_memul_ts_mm_misaligned_block, 'test_softfloat_base':softfloat_memul_ts_mm  }
    argnames = { 'test_base':[ 'vs1', 'vs2' ], 'test_stride':[ 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ], 'test_misaligned_block':[ 'vs1', 'vs2', 'off_s1', 'off_s2', 'off_d' ], 'test_softfloat_base':[ 'vs1', 'vs2' ] }

    class Case_base_inst(Case_base):
        header = '#define TS\n#define HF\n#include "memul.h"'
        def template( self, num, name, vd, vs1, vs2, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[1]}, {vs1_shape[0]}, {vs2_shape[1]} )'
    class Case_stride_inst(Case_stride):
        header = '#define TS\n#define HF\n#include "memul.h"'
        def template( self, num, name, vd, vs1, vs2, stride_s1, stride_s2, stride_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL_STRIDE( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[1]}, {vs1_shape[0]}, {vs2_shape[1]}, {stride_s1}, {stride_s2}, {stride_d} )'
    class Case_misaligned_block_inst(Case_misaligned_block):
        header = '#define TS\n#define HF\n#include "memul.h"'
        def template( self, num, name, vd, vs1, vs2, off_s1, off_s2, off_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL_MISALIGNED_BLOCK( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[1]}, {vs1_shape[0]}, {vs2_shape[1]}, {off_s1}, {off_s2}, {off_d} )'

class Test_memul_x8_mm(BaseTest_memul_mm):
    inst = Memul_x8_mm

    params_base = [
        #*****************************/
        #*      Sanity tests         */
        #*****************************/
        # Small case (4, 4) x (4, 4)
        [ 4, 4, 4 ],
        # Medium case (64, 64) x (64, 64)
        [ 64, 64, 64 ],
        # Large case (256, 256) x (256, 256)
        [ 256, 256, 256 ],

        #*****************************/
        #*       Shape tests         */
        #*****************************/
        # Test dim=1
        # (1, 1) x (1, 1)
        [ 1, 1, 1 ],
        # (1, 1) x (1, 1024)
        [ 1, 1, 1024 ],
        # (1, 1024) x (1024, 1)
        [ 1, 1024, 1 ],
        # (1024, 1) x (1, 1)
        [ 1024, 1, 1 ],
        # (256, 256) x (256, 1)
        [ 256, 256, 1 ],
        # (256, 1) x (1, 256)
        [ 256, 1, 256 ],
        # (1, 256) x (256, 256)
        [ 1, 256, 256 ],

        # Test large dim size
        # (65535, 8)[512k] x (8, 2) = (65535, 1)[256k]
        [ 65535, 8, 1 ],
        # (256, 2048)[512k] x (2048, 256)[512k] = (256, 256)
        [ 256, 2048, 256 ],
        # (1, 8) x (8, 65535)[512k] = (1, 65535)[256k]
        [ 1, 8, 65535 ],

        # Small ordinary shapes
        # (7, 13) x (13, 9)
        [ 7, 13, 9 ],
        # Medium ordinary shapes
        # (52, 73) x (73, 42)
        [ 52, 73, 42 ],
        # Large ordinary shapes
        # (243, 322) x (322, 157)
        [ 243, 322, 157 ],

        # Test blocking edge cases
        [ 63, 65, 65 ],
        [ 65, 63, 65 ],
        [ 65, 65, 63 ],
        [ 63, 63, 65 ],
        [ 63, 65, 63 ],
        [ 65, 63, 63 ],
        [ 65, 65, 65 ],

    ]
    params_stride = [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == width == 128
        [ 64, 64, 64, 64, 64, 256 ],

        # Test src1/src2/dst stride combinations
        # src1 width = 64, stride = 256
        [ 64, 64, 64, 256, 0, 0 ],
        # src2 width = 64, stride = 256
        [ 64, 64, 64, 0, 256, 0 ],
        # dst width = 64, stride = 256
        [ 64, 64, 64, 0, 0, 256 ],
        # src1 and src2 are both strided
        [ 64, 64, 64, 256, 256, 0 ],
        # src1 and dst are both strided
        [ 64, 64, 64, 256, 0, 256 ],
        # src2 and dst are both strided
        [ 64, 64, 64, 0, 256, 256 ],
        # src1, src2 and dst are all strided
        [ 64, 64, 64, 256, 256, 256 ],

        # Test misaligned strides
        [ 64, 64, 64, 230, 154, 520 ],
        # Test misaligned strides with ordinary shapes
        [ 51, 62, 73, 314, 238, 452 ],

        #rs1 row=1, rs1 and rd stride < width test
        [ 1, 64, 64, 17, 0, 17 ],
        #rs2 row=1, rs2 stride < width test
        [ 64, 1, 64, 0, 31, 0 ],
    ]
    params_misaligned_block = [
        #*****************************************/
        #*     Misaligned block address tests    */
        #*  (addresses are not 128-byte aligned) */
        #*****************************************/
        # Test misaligned RS1 address
        [ 64, 64, 64, 2, 0, 0 ],
        # Test misaligned RS2 address
        [ 64, 64, 64, 0, 2, 0 ],
        # Test misaligned RD address
        [ 64, 64, 64, 0, 0, 4 ],
        # Test misaligned RS1/RS2/RD addresses
        [ 64, 64, 64, 18, 28, 8 ],
    ]
    params = { 'test_base': params_base, 'test_stride': params_stride, 'test_misaligned_block': params_misaligned_block,
    'test_softfloat_base': BaseTest_memul_mm.params_softfloat }
    lb = -128
    ub =  127
    data_function = { 'test_base':random_memul_x8_mm, 'test_stride':random_memul_x8_mm_stride, 'test_misaligned_block':random_memul_x8_mm_misaligned_block, 'test_softfloat_base':softfloat_memul_mm }
    argnames = { 'test_base':[ 'vs1', 'vs2' ], 'test_stride':[ 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ], 'test_misaligned_block':[ 'vs1', 'vs2', 'off_s1', 'off_s2', 'off_d' ], 'test_softfloat_base':[ 'vs1', 'vs2' ] }

    class Case_base_inst(Case_base):
        header = '#define X8\n#include "memul.h"'
    class Case_stride_inst(Case_stride):
        header = '#define X8\n#include "memul.h"'
    class Case_misaligned_block_inst(Case_misaligned_block):
        header = '#define X8\n#include "memul.h"'

    def test_softfloat_base( self, vs1, vs2 ):
        pass

class Test_memul_hf_x8_mm(BaseTest_memul_mm):
    inst = Memul_hf_x8_mm
    params_base = [
        #*****************************/
        #*      Sanity tests         */
        #*****************************/
        # Small case (4, 4) x (4, 4)
        [ 4, 4, 4 ],
        # Medium case (64, 64) x (64, 64)
        [ 64, 64, 64 ],
        # Large case (256, 256) x (256, 256)
        [ 256, 256, 256 ],

        #*****************************/
        #*       Shape tests         */
        #*****************************/
        # Test dim=1
        # (1, 1) x (1, 1)
        [ 1, 1, 1 ],
        # (1, 1) x (1, 1024)
        [ 1, 1, 1024 ],
        # (1, 1024) x (1024, 1)
        [ 1, 1024, 1 ],
        # (1024, 1) x (1, 1)
        [ 1024, 1, 1 ],
        # (256, 256) x (256, 1)
        [ 256, 256, 1 ],
        # (256, 1) x (1, 256)
        [ 256, 1, 256 ],
        # (1, 256) x (256, 256)
        [ 1, 256, 256 ],

        # Test large dim size
        # (65535, 8)[512k] x (8, 2) = (65535, 1)[256k]
        [ 65535, 8, 1 ],
        # (128, 2048)[512k] x (2048, 256)[512k] = (256, 256)
        [ 256, 2048, 256 ],
        # (1, 8) x (8, 65535)[512k] = (1, 65535)[256k]
        [ 1, 8, 65535 ],

        # Small ordinary shapes
        # (7, 13) x (13, 9)
        [ 7, 13, 9 ],
        # Medium ordinary shapes
        # (52, 73) x (73, 42)
        [ 52, 73, 42 ],
        # Large ordinary shapes
        # (243, 322) x (322, 157)
        [ 243, 322, 157 ],

        # Test blocking edge cases
        [ 63, 65, 65 ],
        [ 65, 63, 65 ],
        [ 65, 65, 63 ],
        [ 63, 63, 65 ],
        [ 63, 65, 63 ],
        [ 65, 63, 63 ],
        [ 65, 65, 65 ],

        ]
    params_stride = [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == width
        [ 64, 64, 64, 64, 64, 128 ],

        # Test src1/src2/dst stride combinations
        # src1 width = 64, stride = 256
        [ 64, 64, 64, 256, 0, 0 ],
        # src2 width = 64, stride = 256
        [ 64, 64, 64, 0, 256, 0 ],
        # dst width = 64, stride = 256
        [ 64, 64, 64, 0, 0, 256 ],
        # src1 and src2 are both strided
        [ 64, 64, 64, 256, 256, 0 ],
        # src1 and dst are both strided
        [ 64, 64, 64, 256, 0, 256 ],
        # src2 and dst are both strided
        [ 64, 64, 64, 0, 256, 256 ],
        # src1, src2 and dst are all strided
        [ 64, 64, 64, 256, 256, 256 ],

        # Test misaligned strides
        [ 64, 64, 64, 230, 154, 520 ],
        # Test misaligned strides with ordinary shapes
        [ 51, 62, 73, 314, 238, 452 ],

        #rs1 row=1, rs1 and rd stride < width test
        [ 1, 64, 64, 17, 0, 17 ],
        #rs2 row=1, rs2 stride < width test
        [ 64, 1, 64, 0, 31, 0 ],
    ]
    params_misaligned_block = [
        #*****************************************/
        #*     Misaligned block address tests    */
        #*  (addresses are not 128-byte aligned) */
        #*****************************************/
        # Test misaligned RD address
        [ 64, 64, 64, 0, 0, 4 ],
    ]
    params_softfloat = [
        #*****************************/
        #*  Test special FP values   */
        #*****************************/
        # Test dequant coeff = 0
        [ 64, 64, 64, 0.0 ],
        # Test dequant coeff = -0
        [ 64, 64, 64, -0.0 ],
        # Test dequant coeff = +inf
        [ 64, 64, 64, np.float('inf') ],
        # Test dequant coeff = -inf
        [ 64, 64, 64, np.float('-inf') ],
        # Test dequant coeff = nan
        [ 64, 64, 64, np.float('nan') ],
        # Test dequant coeff = 0.1
        [ 64, 64, 64, 0.1 ],
        # Test dequant coeff = 10
        [ 64, 64, 64, 10 ],
        # Test dequant coeff = 65500
        [ 64, 64, 64, 65500 ],
        # Test dequant coeff = 6.104e-05
        [ 64, 64, 64, 6.104e-05 ],
        # Test dequant coeff = 6.e-08
        [ 64, 64, 64, 6.e-08 ],
    ]
    params = { 'test_base': params_base, 'test_stride': params_stride, 'test_misaligned_block': params_misaligned_block,
    'test_softfloat_base': params_softfloat }
    lb = -128
    ub =  127
    data_function = { 'test_base':random_memul_hf_x8_mm, 'test_stride':random_memul_hf_x8_mm_stride, 'test_misaligned_block':random_memul_hf_x8_mm_misaligned_block,
    'test_softfloat_base': softfloat_hf_x8_mm }
    argnames = { 'test_base':[ 'dequant', 'vs1', 'vs2' ], 'test_stride':[ 'dequant', 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ],
    'test_misaligned_block':[ 'dequant', 'vs1', 'vs2', 'off_s1', 'off_s2', 'off_d'], 'test_softfloat_base':[ 'dequant', 'vs1', 'vs2' ] }

    class Case_base_inst(Case_base):
        header = '#define HF_X8\n#include "memul.h"'
        def template( self, num, name, vd, dequant, vs1, vs2, dequant_data, dequant_shape, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]} )'

    class Case_stride_inst(Case_stride):
        header = '#define HF_X8\n#include "memul.h"'
        def template( self, num, name, vd, dequant, vs1, vs2, stride_s1, stride_s2, stride_d, dequant_data, dequant_shape, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL_STRIDE( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {stride_s1}, {stride_s2}, {stride_d} )'

    class Case_misaligned_block_inst(Case_misaligned_block):
        header = '#define HF_X8\n#include "memul.h"'
        def template( self, num, name, vd, dequant, vs1, vs2, off_s1, off_s2, off_d, dequant_data, dequant_shape, vs1_data, vs1_shape, vs2_data, vs2_shape ):
            return f'TEST_MEMUL_MISALIGNED_BLOCK( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {off_s1}, {off_s2}, {off_d} )'

    def test_base( self, dequant, vs1, vs2 ):
        simulate( self, self.Case_base_inst, dequant=dequant, vs1=vs1, vs2=vs2 )

    def test_stride( self, dequant, vs1, vs2, stride_s1, stride_s2, stride_d ):
        simulate( self, self.Case_stride_inst, dequant=dequant, vs1=vs1, vs2=vs2, stride_s1=stride_s1, stride_s2=stride_s2, stride_d=stride_d )

    def test_misaligned_block( self, dequant, vs1, vs2, off_s1, off_s2, off_d ):
        simulate( self, self.Case_misaligned_block_inst, dequant=dequant, vs1=vs1, vs2=vs2, off_s1=off_s1, off_s2=off_s2, off_d=off_d )

    def test_softfloat_base( self, dequant, vs1, vs2 ):
        simulate( self, self.Case_base_inst, dequant=dequant, vs1=vs1, vs2=vs2 )



