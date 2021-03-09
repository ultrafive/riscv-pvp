import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veadd_mm import *
from isa.custom.vesub_mm import *

class Case_basic_shapes(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_INTERNAL({num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]});'

class Case_stride(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, rs1, rs2, dstride, sstride1, sstride2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_STRIDE_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {dstride}, {sstride1}, {sstride2} );'

class Case_inplace_rs1(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_INPLACE_RS1_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} );'

class Case_inplace_rs2(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_INPLACE_RS2_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]} );'

class Case_rs1_eq_rs2(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_INPLACE_RS1_EQ_RS2_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]} );'

class Case_misaligned_base(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, width, height, doff, soff1, soff2):
        return f'TEST_VEXXX_MM_MISALIGNED_BASE( {num}, {name}, {width}, {height}, {doff}, {soff1}, {soff2} )'

class Case_invalid_param(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, width, height ):
        return f'TEST_VEXXX_MM_INVALID_PARAM( {num}, {name}, {width}, {height} )'

class Case_misaligned_stride(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, width, height, dstride, sstride1, sstride2):
        return f'TEST_VEXXX_MM_MISALIGNED_STRIDE( {num}, {name}, {width}, {height}, {dstride}, {sstride1}, {sstride2} )'

class Case_access_fault(BaseCase):
    head = '#include "vexxx_mm.h"'
    def template(self, num, name, rd, width, height, dst, src1, src2):
        return f'TEST_VEXXX_MM_ACCESS_FAULT( {num}, {name}, {width}, {height}, {dst}, {src1}, {src2} )'

class BaseTest_vexxx_mm(BaseTest):
    @pytest.mark.parametrize('rs1, rs2', [
        # Functional tests with basic data
        linspace_mm(np.half, 64, 32 ),
        linspace_mm(np.half, 64, 64 ),
        linspace_mm(np.half, 128, 128 ),
        linspace_mm(np.half, 256, 256 ),
        linspace_mm(np.half, 256, 512 ),

        # Functional tests with shapes

        # near 64 mac
        linspace_mm(np.half, 63, 31 ),
        linspace_mm(np.half, 65, 33 ),
        linspace_mm(np.half, 65, 33 ),
        
        # small shapes
        linspace_mm(np.half, 1, 1 ),
        linspace_mm(np.half, 10, 1 ),
        linspace_mm(np.half, 1, 10 ),
        linspace_mm(np.half, 10, 10 ),

        # middle shapes
        linspace_mm(np.half, 127, 127 ),
        linspace_mm(np.half, 255, 127 ),
        linspace_mm(np.half, 127, 255 ),
        linspace_mm(np.half, 255, 255 ),

        # full of l1buffer
        linspace_mm(np.half, 54613, 4 ),
        linspace_mm(np.half, 853, 256 ),
        linspace_mm(np.half, 256, 853 ),
        
        
        # Functional tests with special float
        special_float_mm(np.half, 32, 1)
    ])
    def test_basic_shapes(self, rs1, rs2 ):
        simulate(self, Case_basic_shapes, rs1=rs1, rs2=rs2)


    @pytest.mark.parametrize('rs1, rs2, dstride, sstride1, sstride2', [
        #functional tests for stride

        linspace_mm_stride( np.half, 64, 32, 128, 0, 0 ),
        linspace_mm_stride( np.half, 64, 32, 0, 128, 0 ),
        linspace_mm_stride( np.half, 64, 32, 0, 0, 128 ),
        linspace_mm_stride( np.half, 64, 32, 0, 128, 128 ),
        linspace_mm_stride( np.half, 64, 32, 128, 128, 0 ),
        linspace_mm_stride( np.half, 64, 32, 128, 128, 128 ),
        linspace_mm_stride( np.half, 63, 31, 130, 130, 130 ),
        linspace_mm_stride( np.half, 65, 33, 254, 254, 254 ),
        linspace_mm_stride( np.half, 63, 33, 126, 126, 126 ),
        # row=1, rs and rd all stride < width test
        linspace_mm_stride( np.half, 63, 1, 23, 19, 7 )
    ] )
    def test_stride(self, rs1, rs2, dstride, sstride1, sstride2 ):
        simulate(self, Case_stride, rs1=rs1, rs2=rs2, dstride=dstride, sstride1=sstride1, sstride2=sstride2 )

    #Inplace compute tests for rd=rs1, rd=rs2, rs1=rs2, rd=rs1=rs2
    @pytest.mark.parametrize('rs1, rs2', [
        # rd = rs1
        linspace_mm( np.half, 4, 4)
    ])
    def test_inplace_rs1( self, rs1, rs2 ):
        simulate( self, Case_inplace_rs1, rs1=rs1, rs2=rs2  )

    @pytest.mark.parametrize('rs1, rs2', [
        # rd = rs2
        linspace_mm( np.half, 16, 4)
    ])
    def test_inplace_rs2( self, rs1, rs2 ):
        simulate( self, Case_inplace_rs2, rs1=rs1, rs2=rs2  )  

    @pytest.mark.parametrize('rs1', [
        # rd = rs1 = rs2
        linspace_mm_rs1_eq_rs2( np.half, 4, 16 )
    ])  
    def test_rs1_eq_rs2( self, rs1 ):
        simulate( self, Case_rs1_eq_rs2, rs1=rs1, rs2=rs1 )

    # Test exception with unaligned base address
    @pytest.mark.parametrize('width, height, doff, soff1, soff2',[
        # rd misaligned
        [ 2, 2, 1, 0, 0 ],
        # rs1 misaligned
        [ 2, 2, 0, 63, 0 ],
        # rs2 misaligned
        [ 2, 2, 0, 0, 65 ],
        # rs1 + rs2 misaligned
        [ 2, 2, 0, 127, 5 ]
    ])
    def test_misaligned_base( self, width, height, doff, soff1, soff2 ):
        simulate( self, Case_misaligned_base, width=width, height=height, doff=doff, soff1=soff1, soff2=soff2 )

    #Test exception with invalid param, width/height=0
    @pytest.mark.parametrize('width, height',[
        # width = 0
        [ 0, 2 ],
        # height = 0
        [ 10, 0 ],
        # height = 0
        [ 64, 0 ],
        # width = 0, height = 0
        [ 0, 0 ]
    ])
    def test_invalid_param( self, width, height ):
        simulate( self, Case_invalid_param, width=width, height=height )

    # Test exception with unaligned stride
    @pytest.mark.parametrize('width, height, dstride, sstride1, sstride2', [
        # rd misaligned
        [ 2, 2, 1, 0, 0 ],
        [ 2, 2, 0, 63, 0 ],
        [ 2, 2, 0, 0, 65 ],
        [ 2, 2, 0, 127, 5 ]
    ])
    def test_misaligned_stride( self, width, height, dstride, sstride1, sstride2 ):
        simulate( self, Case_misaligned_stride, width=width, height=height, dstride=dstride, sstride1=sstride1, sstride2=sstride2 )

    # Test exception with access fault
    @pytest.mark.parametrize('width, height, dst, src1, src2', [
        # rd = 0, ddr
        [ 2, 2, 0,           'RS1_ADDR', 'RS2_ADDR' ],
        # rd in ddr
        [ 2, 2, 0x1000,      'RS1_ADDR', 'RS2_ADDR' ],
        # rd = L1B Base - 1
        [ 2, 2, 0xbffffffe,  'RS1_ADDR', 'RS2_ADDR' ],
        # rd = L1B Max + 1
        [ 2, 2, 0xc0140000,  'RS1_ADDR', 'RS2_ADDR' ],
        # rd = ImB Base - 1
        [ 2, 2, 0xc03ffffe,  'RS1_ADDR', 'RS2_ADDR' ],
        # rd = ImB Max + 1
        [ 2, 2, 0xc0440000,  'RS1_ADDR', 'RS2_ADDR' ],
        # rd in llb
        [ 2, 2, 0xf8001000,  'RS1_ADDR', 'RS2_ADDR' ],

        # rs1 = 0, ddr
        [ 2, 2, 'RD_ADDR',    0,         'RS2_ADDR' ],
        # rs1 in ddr
        [ 2, 2, 'RD_ADDR',    0x1000,    'RS2_ADDR' ],
        # rs1 = L1B Base - 1
        [ 2, 2, 'RD_ADDR',   0xbffffffe, 'RS2_ADDR' ],
        # rs1 = L1B Max + 1
        [ 2, 2, 'RD_ADDR',   0xc0140000, 'RS2_ADDR' ],
        # rs1 = ImB Base - 1
        [ 2, 2, 'RD_ADDR',   0xc03ffffe, 'RS2_ADDR' ],
        # rs1 = ImB Max + 1
        [ 2, 2, 'RD_ADDR',   0xc0440000, 'RS2_ADDR' ],
        # rs1 in llb
        [ 2, 2, 'RD_ADDR',   0xf8001000, 'RS2_ADDR' ],

        # rs2 = 0, ddr
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0         ],
        # rs2 in ddr
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0x1000    ], 
        # rs2 = L1B Base - 1
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0xbffffffe],
        # rs2 = L1B Max + 1
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0xc0140000],
        # rs2 = ImB Base - 1
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0xc03ffffe],
        # rs2 = ImB Max + 1
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0xc0440000],
        # rs2 in llb
        [ 2, 2, 'RD_ADDR',   'RS1_ADDR',  0xf8001000]
    ])
    def test_access_fault( self, width, height, dst, src1, src2 ):
        simulate( self, Case_access_fault, width=width, height=height, dst=dst, src1=src1, src2=src2 )

class Test_veadd_mm(BaseTest_vexxx_mm):
    inst = Veadd_mm

class Test_vesub_mm(BaseTest_vexxx_mm):
    inst = Vesub_mm
  