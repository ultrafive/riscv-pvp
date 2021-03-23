import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veacc_m_dim import *
from isa.custom.vemax_m_dim import *
from isa.custom.vemin_m_dim import *

class BaseCase_VEXXX_M(BaseCase):
    header = '#include "vexxx_m_dim.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    foot = ''


class Case_shape(BaseCase_VEXXX_M):
    def template( self, num, name, rd, rs1, dim, rs1_data, rs1_shape ):
        if dim == 0:
            return f'TEST_VEXXX_M_DIM_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {dim} )'
        else:
            return f'TEST_VEXXX_M_DIM_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[0]}, {rs1_shape[1]}, {dim} )'

class Case_stride(BaseCase_VEXXX_M):
    def template( self, num, name, rd, rs1, sstride1, dim, rs1_data, rs1_shape ):
        if dim == 0:
            return f'TEST_VEXXX_M_DIM_STRIDE_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {dim}, {sstride1} )'
        else:
            return f'TEST_VEXXX_M_DIM_STRIDE_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[0]}, {rs1_shape[1]}, {dim}, {sstride1} )'

class Case_misaligned_base(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, soff1, dim ):
        return f'TEST_VEXXX_M_DIM_MISALIGNED_BASE( {num}, {name}, {width}, {height}, {dim}, {soff1} )'

class Case_invalid_param(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, dim ):
        return f'TEST_VEXXX_M_DIM_INVALID_PARAM( {num}, {name}, {width}, {height}, {dim} )'

class Case_misaligned_stride(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, sstride1, dim ):
        return f'TEST_VEXXX_M_DIM_MISALIGNED_STRIDE( {num}, {name}, {width}, {height}, {dim}, {sstride1} )'

class Case_access_fault(BaseCase_VEXXX_M):
    def template( self, num, name, rd, width, height, src1, dim ):
        return f'TEST_VEXXX_M_DIM_ACCESS_FAULT( {num}, {name}, {width}, {height}, {dim}, {src1} )'


class BaseTest_vexxx_m_dim(BaseTest):

    @pytest.mark.parametrize( 'rs1, dim',[
        # dimh

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 0 ),
        random_m_dim( np.half, 64, 64, 0 ),
        random_m_dim( np.half, 128, 128, 0 ),
        random_m_dim( np.half, 256, 256, 0 ),
        random_m_dim( np.half, 256, 512, 0 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 0 ),
        random_m_dim( np.half, 65, 33, 0 ),
        random_m_dim( np.half, 63, 33, 0 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 0 ),
        random_m_dim( np.half, 10, 1, 0 ),
        random_m_dim( np.half, 1, 10, 0 ),
        random_m_dim( np.half, 10, 10, 0 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 0 ),
        random_m_dim( np.half, 255, 127, 0 ),
        random_m_dim( np.half, 127, 255, 0 ),
        random_m_dim( np.half, 255, 255, 0 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 0 ),
        random_m_dim( np.half, 853, 256, 0 ),
        random_m_dim( np.half, 256, 853, 0 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 0 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 0 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 0 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 0 ),
        # NaN
        special_float_m_dim( np.half, 44, 0x7e00, 0 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 0 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 0 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 0 ),

        # dim_w

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 1 ),
        random_m_dim( np.half, 64, 64, 1 ),
        random_m_dim( np.half, 128, 128, 1 ),
        random_m_dim( np.half, 256, 256, 1 ),
        random_m_dim( np.half, 256, 512, 1 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 1 ),
        random_m_dim( np.half, 65, 33, 1 ),
        random_m_dim( np.half, 63, 33, 1 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 1 ),
        random_m_dim( np.half, 10, 1, 1 ),
        random_m_dim( np.half, 1, 10, 1 ),
        random_m_dim( np.half, 10, 10, 1 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 1 ),
        random_m_dim( np.half, 255, 127, 1 ),
        random_m_dim( np.half, 127, 255, 1 ),
        random_m_dim( np.half, 255, 255, 1 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 1 ),
        random_m_dim( np.half, 853, 256, 1 ),
        random_m_dim( np.half, 256, 853, 1 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 1 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 1 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 1 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 1 ),
        # NaN
        special_float_m_dim( np.half, 44, 0x7e00, 1 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 1 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 1 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 1 )

    ] )
    def test_shape( self, rs1, dim ):
        simulate( self, self.Case_shape_inst, rs1=rs1, dim=dim )

    @pytest.mark.parametrize( 'rs1, sstride1, dim', [
        # dimh

        # functional tests for stride
        random_m_stride_dim( np.half, 64, 32, 0, 0 ),
        random_m_stride_dim( np.half, 64, 32, 130, 0 ),
        random_m_stride_dim( np.half, 64, 32, 128, 0 ),
        random_m_stride_dim( np.half, 64, 32, 256, 0 ),
        random_m_stride_dim( np.half, 64, 32, 512, 0 ),
        random_m_stride_dim( np.half, 64, 32, 1024, 0 ),

        random_m_stride_dim( np.half, 63, 31, 130, 0 ),
        random_m_stride_dim( np.half, 65, 33, 254, 0 ),
        random_m_stride_dim( np.half, 63, 33, 126, 0 ),

        # row=1, rs_stride < width testenv = 'RVTEST_RV32STC'
        random_m_stride_dim( np.half, 63, 1, 13, 0 ),

        # dimw

        # functional tests for stride
        random_m_stride_dim( np.half, 64, 32, 0, 1 ),
        random_m_stride_dim( np.half, 64, 32, 130, 1 ),
        random_m_stride_dim( np.half, 64, 32, 128, 1 ),
        random_m_stride_dim( np.half, 64, 32, 256, 1 ),
        random_m_stride_dim( np.half, 64, 32, 512, 1 ),
        random_m_stride_dim( np.half, 64, 32, 1024, 1 ),

        random_m_stride_dim( np.half, 63, 31, 130, 1 ),
        random_m_stride_dim( np.half, 65, 33, 254, 1 ),
        random_m_stride_dim( np.half, 63, 33, 126, 1 ),

        # row=1, rs_stride < width test
        random_m_stride_dim( np.half, 63, 1, 13, 1 ),
    ] )
    def test_stride( self, rs1, sstride1, dim ):
        simulate( self, self.Case_stride_inst, rs1=rs1, sstride1=sstride1, dim=dim )

    @pytest.mark.parametrize( 'width, height, soff1, dim', [
        #dim_h

        # Test execption with unaligned base address

        # rd misaligned
        [ 2, 2, 1, 0 ],
        # rs1 misaligned
        [ 2, 2, 63, 0 ],
        # rs2 misaligned
        [ 2, 2, 65, 0 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 127, 0 ],

        #dim_w

        # Test execption with unaligned base address

        # rd misaligned
        [ 2, 2, 1, 1 ],
        # rs1 misaligned
        [ 2, 2, 63, 1 ],
        # rs2 misaligned
        [ 2, 2, 65, 1 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 127, 1 ]

    ] )
    def test_misaligned_base( self, width, height, soff1, dim ):
        simulate( self, self.Case_misaligned_base_inst, width=width, height=height, soff1=soff1, dim=dim )

    @pytest.mark.parametrize( 'width, height, dim', [
        # dim_h

        # Test execption with invalid param, width/height=0
 
        # width = 0
        [ 0, 2, 0 ],
        # height = 0
        [ 10, 0, 0 ],
        # height = 0
        [ 64, 0, 0 ],
        # width = 0, height = 0
        [ 0, 0, 0 ],

        #dim_w

        # Test execption with invalid param, width/height=0
 
        # width = 0
        [ 0, 2, 1 ],
        # height = 0
        [ 10, 0, 1 ],
        # height = 0
        [ 64, 0, 1 ],
        # width = 0, height = 0
        [ 0, 0, 1 ],
    ])
    def test_invalid_param( self, width, height, dim ):
        simulate( self, self.Case_invalid_param_inst, width=width, height=height, dim=dim )

    @pytest.mark.parametrize( 'width, height, sstride1, dim', [
        # dim_h

        # Test execption with unaligned stride
        
        # rd misaligned
        [ 2, 2, 1, 0 ],
        # rs1 misaligned
        [ 2, 2, 63, 0 ],
        # rs2 misaligned
        [ 2, 2, 65, 0 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 127, 0 ],

        #dim_w

        # Test execption with unaligned stride
        
        # rd misaligned
        [ 2, 2, 1, 1 ],
        # rs1 misaligned
        [ 2, 2, 63, 1 ],
        # rs2 misaligned
        [ 2, 2, 65, 1 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 127, 1 ],
    ] )
    def test_misaligned_stride( self, width, height, sstride1, dim ):
        simulate( self, self.Case_misaligned_stride_inst, width=width, height=height, sstride1=sstride1, dim=dim )

    @pytest.mark.parametrize( 'width, height, src1, dim', [
        #dim_h

        # Test execption with access fault
        
        # rs1 = 0, ddr
        [ 2, 2, 0         , 0 ],
        # rs1 in ddr
        [ 2, 2, 0x1000    , 0 ],
        # rs1 = L1B Base - 1
        [ 2, 2, 0xbffffffe, 0 ],
        # rs1 = L1B Max + 1
        [ 2, 2, 0xc0140000, 0 ],
        # rs1 = ImB Base - 1
        [ 2, 2, 0xc03ffffe, 0 ],
        # rs1 = ImB Max + 1
        [ 2, 2, 0xc0440000, 0 ],
        # rs1 in llb
        [ 2, 2, 0xf8001000, 0 ],

        #dim_w

        # Test execption with access fault
        
        # rs1 = 0, ddr
        [ 2, 2, 0         , 1 ],
        # rs1 in ddr
        [ 2, 2, 0x1000    , 1 ],
        # rs1 = L1B Base - 1
        [ 2, 2, 0xbffffffe, 1 ],
        # rs1 = L1B Max + 1
        [ 2, 2, 0xc0140000, 1 ],
        # rs1 = ImB Base - 1
        [ 2, 2, 0xc03ffffe, 1 ],
        # rs1 = ImB Max + 1
        [ 2, 2, 0xc0440000, 1 ],
        # rs1 in llb
        [ 2, 2, 0xf8001000, 1 ],
    ] )
    def test_access_fault( self, width, height, src1, dim ):
        simulate( self, self.Case_access_fault_inst, width=width, height=height, src1=src1, dim=dim )

class Test_veacc_m_dim(BaseTest_vexxx_m_dim):
    inst = Veacc_m_dim

    class Case_access_fault_inst(Case_access_fault):
        header = '#include "veacc_m_dim.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        header = '#include "veacc_m_dim.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        header = '#include "veacc_m_dim.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        header = '#include "veacc_m_dim.h"'
    class Case_shape_inst(Case_shape):
        header = '#include "veacc_m_dim.h"'
    class Case_stride_inst(Case_stride):
        header = '#include "veacc_m_dim.h"'

class Test_vemax_m_dim(BaseTest_vexxx_m_dim):
    inst = Vemax_m_dim

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

    @pytest.mark.parametrize( 'rs1, dim',[
        # dimh

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 0 ),
        random_m_dim( np.half, 64, 64, 0 ),
        random_m_dim( np.half, 128, 128, 0 ),
        random_m_dim( np.half, 256, 256, 0 ),
        random_m_dim( np.half, 256, 512, 0 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 0 ),
        random_m_dim( np.half, 65, 33, 0 ),
        random_m_dim( np.half, 63, 33, 0 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 0 ),
        random_m_dim( np.half, 10, 1, 0 ),
        random_m_dim( np.half, 1, 10, 0 ),
        random_m_dim( np.half, 10, 10, 0 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 0 ),
        random_m_dim( np.half, 255, 127, 0 ),
        random_m_dim( np.half, 127, 255, 0 ),
        random_m_dim( np.half, 255, 255, 0 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 0 ),
        random_m_dim( np.half, 853, 256, 0 ),
        random_m_dim( np.half, 256, 853, 0 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 0 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 0 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 0 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 0 ),
        # NaN
        #special_float_m_dim( np.half, 44, 0x7e00, 0 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 0 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 0 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 0 ),

        # dim_w

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 1 ),
        random_m_dim( np.half, 64, 64, 1 ),
        random_m_dim( np.half, 128, 128, 1 ),
        random_m_dim( np.half, 256, 256, 1 ),
        random_m_dim( np.half, 256, 512, 1 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 1 ),
        random_m_dim( np.half, 65, 33, 1 ),
        random_m_dim( np.half, 63, 33, 1 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 1 ),
        random_m_dim( np.half, 10, 1, 1 ),
        random_m_dim( np.half, 1, 10, 1 ),
        random_m_dim( np.half, 10, 10, 1 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 1 ),
        random_m_dim( np.half, 255, 127, 1 ),
        random_m_dim( np.half, 127, 255, 1 ),
        random_m_dim( np.half, 255, 255, 1 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 1 ),
        random_m_dim( np.half, 853, 256, 1 ),
        random_m_dim( np.half, 256, 853, 1 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 1 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 1 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 1 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 1 ),
        # NaN
        #special_float_m_dim( np.half, 44, 0x7e00, 1 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 1 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 1 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 1 )

    ] )
    def test_shape( self, rs1, dim ):
        simulate( self, self.Case_shape_inst, rs1=rs1, dim=dim )

class Test_vemin_m_dim(BaseTest_vexxx_m_dim):
    inst = Vemin_m_dim

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

    @pytest.mark.parametrize( 'rs1, dim',[
        # dimh

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 0 ),
        random_m_dim( np.half, 64, 64, 0 ),
        random_m_dim( np.half, 128, 128, 0 ),
        random_m_dim( np.half, 256, 256, 0 ),
        random_m_dim( np.half, 256, 512, 0 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 0 ),
        random_m_dim( np.half, 65, 33, 0 ),
        random_m_dim( np.half, 63, 33, 0 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 0 ),
        random_m_dim( np.half, 10, 1, 0 ),
        random_m_dim( np.half, 1, 10, 0 ),
        random_m_dim( np.half, 10, 10, 0 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 0 ),
        random_m_dim( np.half, 255, 127, 0 ),
        random_m_dim( np.half, 127, 255, 0 ),
        random_m_dim( np.half, 255, 255, 0 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 0 ),
        random_m_dim( np.half, 853, 256, 0 ),
        random_m_dim( np.half, 256, 853, 0 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 0 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 0 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 0 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 0 ),
        # NaN
        #special_float_m_dim( np.half, 44, 0x7e00, 0 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 0 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 0 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 0 ),

        # dim_w

        # Functional tests with basic data
        random_m_dim( np.half, 64, 32, 1 ),
        random_m_dim( np.half, 64, 64, 1 ),
        random_m_dim( np.half, 128, 128, 1 ),
        random_m_dim( np.half, 256, 256, 1 ),
        random_m_dim( np.half, 256, 512, 1 ),

        # Functional tests with shapes

        # near 64 mac
        random_m_dim( np.half, 63, 31, 1 ),
        random_m_dim( np.half, 65, 33, 1 ),
        random_m_dim( np.half, 63, 33, 1 ),
        
        # small shapes
        random_m_dim( np.half, 1, 1, 1 ),
        random_m_dim( np.half, 10, 1, 1 ),
        random_m_dim( np.half, 1, 10, 1 ),
        random_m_dim( np.half, 10, 10, 1 ),

        # middle shape
        random_m_dim( np.half, 127, 127, 1 ),
        random_m_dim( np.half, 255, 127, 1 ),
        random_m_dim( np.half, 127, 255, 1 ),
        random_m_dim( np.half, 255, 255, 1 ),

        # full of l1buffer
        random_m_dim( np.half, 40960, 8, 1 ),
        random_m_dim( np.half, 853, 256, 1 ),
        random_m_dim( np.half, 256, 853, 1 ),

        # functional tests with special float
        
        # 0
        special_float_m_dim( np.half, 40, 0x0000, 1 ),
        #-0#include "vexxx_m_all.h"
        special_float_m_dim( np.half, 41, 0x8000, 1 ),
        # inf
        special_float_m_dim( np.half, 42, 0x7c00, 1 ),
        # -inf
        special_float_m_dim( np.half, 43, 0xfc00, 1 ),
        # NaN
        #special_float_m_dim( np.half, 44, 0x7e00, 1 ),
        # 65500
        special_float_m_dim( np.half, 45, 0x7bff, 1 ),
        # 6.104e-05
        special_float_m_dim( np.half, 46, 0x0400, 1 ),
        # 6.e-08
        special_float_m_dim( np.half, 47, 0x0001, 1 )

    ] )
    def test_shape( self, rs1, dim ):
        simulate( self, self.Case_shape_inst, rs1=rs1, dim=dim )