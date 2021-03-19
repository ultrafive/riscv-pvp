import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veadd_mf import *
from isa.custom.vesub_mf import *
from isa.custom.veemul_mf import *
from isa.custom.veemul_x32_mf import *
from isa.custom.veemul_x8_hf_mf import *
from isa.custom.vemax_mf import *
from isa.custom.vemin_mf import *

class BaseCase_vexxx_mf(BaseCase):
    head = '#include "vexxx_mf.h"'
    env = 'RVTEST_RV32STC'

class Case_shape(BaseCase_vexxx_mf):
    def template( self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'VEXXX_MF( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} )'


class Case_stride(BaseCase_vexxx_mf):
    def template( self, num, name, rd, rs1, rs2, stride_s1, stride_rd, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'VEXXX_MF_STRIDE( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s1}, {stride_rd} )'

class Case_addr_overlapping(BaseCase_vexxx_mf):
    def template( self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'VEXXX_MF_RS1_RD_OVERLAPPING( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} )'

class Case_misaligned_base_addr(BaseCase_vexxx_mf):
    def template( self, num, name, rd, height, width, off_s1, off_d ):
        return f'VEXXX_MF_MISALIGNED_BASE_ADDR( {num}, {name}, {height}, {width}, {off_s1}, {off_d} )'

class Case_misaligned_stride(BaseCase_vexxx_mf):
    def template( self, num, name, rd, height, width, stride_s1, stride_rd ):
        return f'VEXXX_MF_MISALIGNED_STRIDE( {num}, {name}, {height}, {width}, {stride_s1}, {stride_rd} )'

class Case_invalid_param(BaseCase_vexxx_mf):
    def template( self, num, name, rd, height, width ):
        return f'VEXXX_MF_INVALID_PARAM( {num}, {name}, {height}, {width} )'

class Case_access_fault(BaseCase_vexxx_mf):
    def template( self, num, name, rd, result, val1, val2, height, width ):
        return f'VEXXX_MF_ACCESS_FAULT( {num}, {name}, {result}, {val1}, {val2}, {height}, {width} )'

class BaseTest_vexxx_mf(BaseTest):

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test shapes

        # small shapes, m(odd, odd)
        random_mf( 1, 1 ),
        random_mf( 1, 3 ),
        random_mf( 3, 1 ),
        random_mf( 3, 3 ),

        # m(even, even)
        random_mf( 2, 10 ),
        random_mf( 10, 2 ),
        random_mf( 2, 2 ),
        random_mf( 10, 10 ),

        # m(odd, even), m(even, odd)
        random_mf( 19, 28 ),
        random_mf( 28, 19 ),

        # 64 MAC Engine boundray
        random_mf( 31, 63 ),
        random_mf( 32, 64 ),
        random_mf( 33, 65 ),

        # middle shapes
        random_mf( 35, 129 ),
        random_mf( 36, 257 ),
        random_mf( 131, 38 ),
        random_mf( 258, 260 ),

        # full of L1 buffer
        random_mf( 5, 32767 ),
        random_mf( 320, 512 ),
        random_mf( 512, 320 ),
    ])
    def test_shape( self, rs1, rs2 ):
        simulate( self, self.Case_shape_inst, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'rs1, rs2, stride_s1, stride_rd', [
        # test stride, stride >= ESIZE*width
        random_mf_stride( 15, 15, 30, 0 ),
        random_mf_stride( 15, 15, 0, 30 ),
        random_mf_stride( 15, 15, 30, 30 ),

        random_mf_stride( 34, 34, 130, 0 ),
        random_mf_stride( 34, 34, 0, 130 ),
        random_mf_stride( 34, 34, 130, 130 ),

        random_mf_stride( 61, 63, 128, 130 ),
        random_mf_stride( 66, 64, 210, 150 ),
        random_mf_stride( 127, 65, 262, 200 ),
        # row=1, stride < width test
        random_mf_stride( 1, 65, 35, 200 )
    ] )
    def test_stride( self, rs1, rs2, stride_s1, stride_rd ):
        simulate( self, self.Case_stride_inst, rs1=rs1, rs2=rs2, stride_s1=stride_s1, stride_rd=stride_rd )

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test rd addr = rs1 addr
        random_mf( 24, 23 )
    ] )
    def test_addr_overlapping( self, rs1, rs2 ):
        simulate( self, self.Case_addr_overlapping_inst, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'height, width, off_s1, off_d', [
        # exception test with misaligned base addr

        # rs1 misaligned
        [ 31, 32, 0, 1 ],
        # rd misaligned
        [ 31, 32, 1, 0 ],
        # rs1 and rd misaligned
        [ 31, 32, 1, 1 ],
    ] )
    def test_misaligned_base_addr( self, height, width, off_s1, off_d ):
        simulate( self, self.Case_misaligned_base_addr_inst, height=height, width=width, off_s1=off_s1, off_d=off_d )

    @pytest.mark.parametrize( 'height, width, stride_s1, stride_rd', [
        # exception test with misaligned stride

        # rs1 misaligned
        [ 12, 13, 27, 0 ],
        # rd misaligned
        [ 12, 13, 0, 27 ],
        # rs1 and rd misaligned
        [ 12, 13, 27, 27 ],
        # rd stride < width*ESIZE
        [ 12, 13, 0, '12*ESIZE_OUT' ],
    ] )
    def test_misaligned_stride( self, height, width, stride_s1, stride_rd ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, stride_s1=stride_s1, stride_rd=stride_rd )

    @pytest.mark.parametrize( 'height, width', [
        # exception test with invalid params

        # height = 0
        [ 0, 2 ],
        # width = 0
        [ 3, 0 ],
        # height = width = 0
        [ 0, 0]
    ] )
    def test_invalid_param( self, height, width ):
        simulate( self, self.Case_invalid_param_inst, height=height, width=width )

    @pytest.mark.parametrize( 'result, val1, val2, height, width', [
        # Exception test with access fault

        #rd in ddr 1k
        [ 0x400,  'RS1_ADDR',  'RS2_ADDR', 3, 3 ],

        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 0xbffffffc,  'RS1_ADDR',  'RS2_ADDR', 32, 32 ],

        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 0xc013fffc,  'RS1_ADDR',  'RS2_ADDR', 12, 24 ],

        #rd span from reserved to IB，0xc0400000 - 4 = 0xc03ffffc
        [ 0xc03ffffc,  'RS1_ADDR',  'RS2_ADDR', 8, 8 ],

        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0xc043fffc,  'RS1_ADDR',  'RS2_ADDR', 8, 8 ],

        #rs1 in ddr 1k
        [  'RD_ADDR', 0x400,  'RS2_ADDR', 3, 3 ],

        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [  'RD_ADDR', 0xbffffffc,  'RS2_ADDR', 32, 32 ],

        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [  'RD_ADDR', 0xc013fffc,  'RS2_ADDR', 12, 24 ],

        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [  'RD_ADDR', 0xc03ffffc,  'RS2_ADDR', 8, 8 ],

        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [  'RD_ADDR', 0xc043fffc,  'RS2_ADDR', 8, 8 ],
    ] )
    def test_access_fault( self, result, val1, val2, height, width ):
        simulate( self, self.Case_access_fault_inst, result=result, val1=val1, val2=val2, height=height, width=width )
    

class Test_veadd_mf(BaseTest_vexxx_mf):
    inst = Veadd_mf
    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

class Test_vesub_mf(BaseTest_vexxx_mf):
    inst = Vesub_mf
    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

class Test_veemul_mf(BaseTest_vexxx_mf):
    inst = Veemul_mf

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

class Test_veemul_x32_mf(BaseTest_vexxx_mf):
    inst = Veemul_x32_mf

    class Case_access_fault_inst(Case_access_fault):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_shape_inst(Case_shape):
        head = '#define X32_MF\n#include "vexxx_mf.h"'
    class Case_stride_inst(Case_stride):
        head = '#define X32_MF\n#include "vexxx_mf.h"'

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test shapes

        # small shapes, m(odd, odd)
        random_mf_x32( 1, 1 ),
        random_mf_x32( 1, 3 ),
        random_mf_x32( 3, 1 ),
        random_mf_x32( 3, 3 ),

        # m(even, even)
        random_mf_x32( 2, 10 ),
        random_mf_x32( 10, 2 ),
        random_mf_x32( 2, 2 ),
        random_mf_x32( 10, 10 ),

        # m(odd, even), m(even, odd)
        random_mf_x32( 19, 28 ),
        random_mf_x32( 28, 19 ),

        # 64 MAC Engine boundray
        random_mf_x32( 31, 63 ),
        random_mf_x32( 32, 64 ),
        random_mf_x32( 33, 65 ),

        # middle shapes
        random_mf_x32( 35, 129 ),
        random_mf_x32( 36, 257 ),
        random_mf_x32( 131, 38 ),
        random_mf_x32( 258, 260 ),

        # full of L1 buffer
        random_mf_x32( 5, 32767 ),
        random_mf_x32( 320, 512 ),
        random_mf_x32( 512, 320 ),
    ])
    def test_shape( self, rs1, rs2 ):
        simulate( self, self.Case_shape_inst, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'rs1, rs2, stride_s1, stride_rd', [
        # test stride, stride >= ESIZE*width
        random_mf_stride_x32( 15, 15, 60, 0 ),
        random_mf_stride_x32( 15, 15, 0, 60 ),
        random_mf_stride_x32( 15, 15, 60, 60 ),

        random_mf_stride_x32( 34, 34, 260, 0 ),
        random_mf_stride_x32( 34, 34, 0, 260 ),
        random_mf_stride_x32( 34, 34, 260, 260 ),

        random_mf_stride_x32( 61, 63, 256, 260 ),
        random_mf_stride_x32( 66, 64, 420, 300 ),
        random_mf_stride_x32( 127, 65, 524, 400 ),
        # row=1, rs and rd stride < width test
        random_mf_stride_x32( 1, 65, 35, 17 )
    ] )
    def test_stride( self, rs1, rs2, stride_s1, stride_rd ):
        simulate( self, self.Case_stride_inst, rs1=rs1, rs2=rs2, stride_s1=stride_s1, stride_rd=stride_rd )

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test rd addr = rs1 addr
        random_mf_x32( 24, 23 )
    ] )
    def test_addr_overlapping( self, rs1, rs2 ):
        simulate( self, self.Case_addr_overlapping_inst, rs1=rs1, rs2=rs2 )

class Test_veemul_x8_hf_mf(BaseTest_vexxx_mf):
    inst = Veemul_x8_hf_mf

    class Case_access_fault_inst(Case_access_fault):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_shape_inst(Case_shape):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'
    class Case_stride_inst(Case_stride):
        head = '#define X8_HF_MF\n#include "vexxx_mf.h"'

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test shapes

        # small shapes, m(odd, odd)
        random_mf_x8_hf( 1, 1 ),
        random_mf_x8_hf( 1, 3 ),
        random_mf_x8_hf( 3, 1 ),
        random_mf_x8_hf( 3, 3 ),

        # m(even, even)
        random_mf_x8_hf( 2, 10 ),
        random_mf_x8_hf( 10, 2 ),
        random_mf_x8_hf( 2, 2 ),
        random_mf_x8_hf( 10, 10 ),

        # m(odd, even), m(even, odd)
        random_mf_x8_hf( 19, 28 ),
        random_mf_x8_hf( 28, 19 ),

        # 64 MAC Engine boundray
        random_mf_x8_hf( 31, 63 ),
        random_mf_x8_hf( 32, 64 ),
        random_mf_x8_hf( 33, 65 ),

        # middle shapes
        random_mf_x8_hf( 35, 129 ),
        random_mf_x8_hf( 36, 257 ),
        random_mf_x8_hf( 131, 38 ),
        random_mf_x8_hf( 258, 260 ),

        # full of L1 buffer
        random_mf_x8_hf( 5, 32767 ),
        random_mf_x8_hf( 320, 512 ),
        random_mf_x8_hf( 512, 320 ),
    ])
    def test_shape( self, rs1, rs2 ):
        simulate( self, self.Case_shape_inst, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'rs1, rs2, stride_s1, stride_rd', [
        # test stride, stride >= ESIZE*width
        random_mf_stride_x8_hf( 15, 15, 30, 0 ),
        random_mf_stride_x8_hf( 15, 15, 0, 30 ),
        random_mf_stride_x8_hf( 15, 15, 30, 30 ),

        random_mf_stride_x8_hf( 34, 34, 130, 0 ),
        random_mf_stride_x8_hf( 34, 34, 0, 130 ),
        random_mf_stride_x8_hf( 34, 34, 130, 130 ),

        random_mf_stride_x8_hf( 61, 63, 128, 130 ),
        random_mf_stride_x8_hf( 66, 64, 210, 150 ),
        random_mf_stride_x8_hf( 127, 65, 262, 200 ),
        # row=1, stride < width test
        random_mf_stride_x8_hf( 1, 65, 35, 200 )
    ] )
    def test_stride( self, rs1, rs2, stride_s1, stride_rd ):
        simulate( self, self.Case_stride_inst, rs1=rs1, rs2=rs2, stride_s1=stride_s1, stride_rd=stride_rd )

    @pytest.mark.parametrize( 'rs1, rs2', [
        # test rd addr = rs1 addr
        random_mf_x8_hf( 24, 23 )
    ] )
    def test_addr_overlapping( self, rs1, rs2 ):
        simulate( self, self.Case_addr_overlapping_inst, rs1=rs1, rs2=rs2 )

    @pytest.mark.parametrize( 'height, width, off_s1, off_d', [
        # exception test with misaligned base addr

        # rd misaligned
        [ 31, 32, 1, 0 ],
    ] )
    def test_misaligned_base_addr( self, height, width, off_s1, off_d ):
        simulate( self, self.Case_misaligned_base_addr_inst, height=height, width=width, off_s1=off_s1, off_d=off_d )

    @pytest.mark.parametrize( 'height, width, stride_s1, stride_rd', [
        # exception test with misaligned stride

        # rs1 misaligned
        [ 12, 13, 27, 0 ],
        # rs1 and rd misaligned
        [ 12, 13, 27, 27 ],
        # rd stride < width*ESIZE
        [ 12, 13, 0, '12*ESIZE_OUT' ],
    ] )
    def test_misaligned_stride( self, height, width, stride_s1, stride_rd ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, stride_s1=stride_s1, stride_rd=stride_rd )

class Test_vemin_mf(BaseTest_vexxx_mf):
    inst = Vemin_mf

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass

class Test_vemax_mf(BaseTest_vexxx_mf):
    inst = Vemax_mf

    class Case_access_fault_inst(Case_access_fault):
        pass
    class Case_addr_overlapping_inst(Case_addr_overlapping):
        pass
    class Case_invalid_param_inst(Case_invalid_param):
        pass
    class Case_misaligned_base_addr_inst(Case_misaligned_base_addr):
        pass
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        pass
    class Case_shape_inst(Case_shape):
        pass
    class Case_stride_inst(Case_stride):
        pass