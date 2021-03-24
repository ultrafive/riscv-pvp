import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veacc_m import *
from isa.custom.vemax_m_all import *
from isa.custom.vemin_m_all import *

class BaseCase_VEXXX_M(BaseCase):
    header = '#include "vexxx_m_all.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    footer = ''

class Case_shape(BaseCase_VEXXX_M):
    def template( self, num, name, rd, rs1, rs1_data, rs1_shape ):
        return f'TEST_VEXXX_M_ALL_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]} )'

class Case_stride(BaseCase_VEXXX_M):
    def template( self, num, name, rd, rs1, sstride1, rs1_data, rs1_shape ):
        return f'TEST_VEXXX_M_ALL_STRIDE_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {sstride1} )'

class Case_misaligned_base(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, soff1 ):
        return f'TEST_VEXXX_M_ALL_MISALIGNED_BASE( {num}, {name}, {width}, {height}, {soff1} )'

class Case_invalid_param(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height ):
        return f'TEST_VEXXX_M_ALL_INVALID_PARAM( {num}, {name}, {width}, {height} )'

class Case_misaligned_stride(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, sstride1 ):
        return f'TEST_VEXXX_M_ALL_MISALIGNED_STRIDE( {num}, {name}, {width}, {height}, {sstride1} )'

class Case_access_fault(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, src1 ):
        return f'TEST_VEXXX_M_ALL_ACCESS_FAULT( {num}, {name}, {width}, {height}, {src1} )'


class BaseTest_vexxx_m_all(BaseTest):

    @pytest.mark.parametrize( 'rs1',[
        # Functional tests with basic data
        random_m( np.half, 64, 32 ),
        random_m( np.half, 64, 64 ),
        random_m( np.half, 128, 128 ),
        random_m( np.half, 256, 256 ),
        random_m( np.half, 256, 512 ),

        # Functional tests with shapes

        # near 64 mac
        random_m( np.half, 63, 31 ),
        random_m( np.half, 65, 33 ),
        random_m( np.half, 63, 33 ),
        
        # small shapes
        random_m( np.half, 1, 1 ),
        random_m( np.half, 10, 1 ),
        random_m( np.half, 1, 10 ),
        random_m( np.half, 10, 10 ),

        # middle shape
        random_m( np.half, 127, 127 ),
        random_m( np.half, 255, 127 ),
        random_m( np.half, 127, 255 ),
        random_m( np.half, 255, 255 ),

        # full of l1buffer
        random_m( np.half, 40960, 8 ),
        random_m( np.half, 853, 256 ),
        random_m( np.half, 256, 853 ),

        # functional tests with special float
        
        # 0
        special_float_m( np.half, 40, 0x0000 ),
        #-0#include "vexxx_m_all.h"
        special_float_m( np.half, 41, 0x8000 ),
        # inf
        special_float_m( np.half, 42, 0x7c00 ),
        # -inf
        special_float_m( np.half, 43, 0xfc00 ),
        # NaN
        special_float_m( np.half, 44, 0x7e00 ),
        # 65500
        special_float_m( np.half, 45, 0x7bff ),
        # 6.104e-05
        special_float_m( np.half, 46, 0x0400 ),
        # 6.e-08
        special_float_m( np.half, 47, 0x0001 )

    ] )
    def test_shape( self, rs1 ):
        simulate( self, self.Case_shape_inst, rs1=rs1 )

    @pytest.mark.parametrize( 'rs1, sstride1', [
        # functional tests for stride
        random_m_stride( np.half, 64, 32, 0 ),
        random_m_stride( np.half, 64, 32, 130 ),
        random_m_stride( np.half, 64, 32, 128 ),
        random_m_stride( np.half, 64, 32, 256 ),
        random_m_stride( np.half, 64, 32, 512 ),
        random_m_stride( np.half, 64, 32, 1024 ),

        random_m_stride( np.half, 63, 31, 130 ),
        random_m_stride( np.half, 65, 33, 254 ),
        random_m_stride( np.half, 63, 33, 126 ),

        # row=1, rs_stride < width test
        random_m_stride( np.half, 63, 1, 13 ),

    ] )
    def test_stride( self, rs1, sstride1 ):
        simulate( self, self.Case_stride_inst, rs1=rs1, sstride1=sstride1 )

    @pytest.mark.parametrize( 'width, height, soff1', [
        # Test execption with unaligned base address

        # rd misaligned
        [ 2, 2, 1],
        # rs1 misaligned
        [ 2, 2, 63],
        # rs2 misaligned
        [ 2, 2, 65],
        # rs1 + rs2 misaligned
        [ 2, 2, 127]

    ] )
    def test_misaligned_base( self, width, height, soff1 ):
        simulate( self, self.Case_misaligned_base_inst, width=width, height=height, soff1=soff1 )

    @pytest.mark.parametrize( 'width, height', [
        # Test execption with invalid param, width/height=0
 
        # width = 0
        [ 0, 2],
        # height = 0
        [ 10, 0],
        # height = 0
        [ 64, 0],
        # width = 0, height = 0
        [ 0, 0],
    ])
    def test_invalid_param( self, width,height ):
        simulate( self, self.Case_invalid_param_inst, width=width, height=height )

    @pytest.mark.parametrize( 'width, height, sstride1', [
        # Test execption with unaligned stride
        
        # rd misaligned
        [ 2, 2, 1],
        # rs1 misaligned
        [ 2, 2, 63],
        # rs2 misaligned
        [ 2, 2, 65],
        # rs1 + rs2 misaligned
        [ 2, 2, 127],
    ] )
    def test_misaligned_stride( self, width, height, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, width=width, height=height, sstride1=sstride1 )

    @pytest.mark.parametrize( 'width, height, src1', [

        # Test execption with access fault
        
        # rs1 = 0, ddr
        [ 2, 2, 0         ],
        # rs1 in ddr
        [ 2, 2, 0x1000    ],
        # rs1 = L1B Base - 1
        [ 2, 2, 0xbffffffe],
        # rs1 = L1B Max + 1
        [ 2, 2, 0xc0140000],
        # rs1 = ImB Base - 1
        [ 2, 2, 0xc03ffffe],
        # rs1 = ImB Max + 1
        [ 2, 2, 0xc0440000],
        # rs1 in llb
        [ 2, 2, 0xf8001000],
    ] )
    def test_access_fault( self, width, height, src1 ):
        simulate( self, self.Case_access_fault_inst, width=width, height=height, src1=src1 )

class Test_veacc_m_all(BaseTest_vexxx_m_all):
    inst = Veacc_m

    class Case_access_fault_inst(Case_access_fault):
        header = '#include "veacc_m_all.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        header = '#include "veacc_m_all.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        header = '#include "veacc_m_all.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        header = '#include "veacc_m_all.h"'
    class Case_shape_inst(Case_shape):
        header = '#include "veacc_m_all.h"'
    class Case_stride_inst(Case_stride):
        header = '#include "veacc_m_all.h"'

class Test_vemax_m_all(BaseTest_vexxx_m_all):
    inst = Vemax_m_all

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

    @pytest.mark.parametrize( 'rs1',[
        # Functional tests with basic data
        random_m( np.half, 64, 32 ),
        random_m( np.half, 64, 64 ),
        random_m( np.half, 128, 128 ),
        random_m( np.half, 256, 256 ),
        random_m( np.half, 256, 512 ),

        # Functional tests with shapes

        # near 64 mac
        random_m( np.half, 63, 31 ),
        random_m( np.half, 65, 33 ),
        random_m( np.half, 63, 33 ),
        
        # small shapes
        random_m( np.half, 1, 1 ),
        random_m( np.half, 10, 1 ),
        random_m( np.half, 1, 10 ),
        random_m( np.half, 10, 10 ),

        # middle shape
        random_m( np.half, 127, 127 ),
        random_m( np.half, 255, 127 ),
        random_m( np.half, 127, 255 ),
        random_m( np.half, 255, 255 ),

        # full of l1buffer
        random_m( np.half, 40960, 8 ),
        random_m( np.half, 853, 256 ),
        random_m( np.half, 256, 853 ),

        # functional tests with special float
        
        # 0
        special_float_m( np.half, 40, 0x0000 ),
        #-0#include "vexxx_m_all.h"
        special_float_m( np.half, 41, 0x8000 ),
        # inf
        special_float_m( np.half, 42, 0x7c00 ),
        # -inf
        special_float_m( np.half, 43, 0xfc00 ),
        # 65500
        special_float_m( np.half, 45, 0x7bff ),
        # 6.104e-05
        special_float_m( np.half, 46, 0x0400 ),
        # 6.e-08
        special_float_m( np.half, 47, 0x0001 )

    ] )
    def test_shape( self, rs1 ):
        simulate( self, self.Case_shape_inst, rs1=rs1 )

class Test_vemin_m_all(BaseTest_vexxx_m_all):
    inst = Vemin_m_all

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_inst(Case_misaligned_base):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

    @pytest.mark.parametrize( 'rs1',[
        # Functional tests with basic data
        random_m( np.half, 64, 32 ),
        random_m( np.half, 64, 64 ),
        random_m( np.half, 128, 128 ),
        random_m( np.half, 256, 256 ),
        random_m( np.half, 256, 512 ),

        # Functional tests with shapes

        # near 64 mac
        random_m( np.half, 63, 31 ),
        random_m( np.half, 65, 33 ),
        random_m( np.half, 63, 33 ),
        
        # small shapes
        random_m( np.half, 1, 1 ),
        random_m( np.half, 10, 1 ),
        random_m( np.half, 1, 10 ),
        random_m( np.half, 10, 10 ),

        # middle shape
        random_m( np.half, 127, 127 ),
        random_m( np.half, 255, 127 ),
        random_m( np.half, 127, 255 ),
        random_m( np.half, 255, 255 ),

        # full of l1buffer
        random_m( np.half, 40960, 8 ),
        random_m( np.half, 853, 256 ),
        random_m( np.half, 256, 853 ),

        # functional tests with special float
        
        # 0
        special_float_m( np.half, 40, 0x0000 ),
        #-0#include "vexxx_m_all.h"
        special_float_m( np.half, 41, 0x8000 ),
        # inf
        special_float_m( np.half, 42, 0x7c00 ),
        # -inf
        special_float_m( np.half, 43, 0xfc00 ),
        # 65500
        special_float_m( np.half, 45, 0x7bff ),
        # 6.104e-05
        special_float_m( np.half, 46, 0x0400 ),
        # 6.e-08
        special_float_m( np.half, 47, 0x0001 )

    ] )
    def test_shape( self, rs1 ):
        simulate( self, self.Case_shape_inst, rs1=rs1 )