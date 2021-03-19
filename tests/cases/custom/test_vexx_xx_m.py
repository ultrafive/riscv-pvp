import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.vecvt_hf_x8_m import *
from isa.custom.vecvt_hf_xu8_m import *
from isa.custom.vecvt_x8_hf_m import *
from isa.custom.veexp_m import *
from isa.custom.vesqrt_m import *
from isa.custom.verecip_m import *

class BaseCase_VEXX_XX_M(BaseCase):
    head = '#include "vexx_xx_m.h"'
    env = 'RVTEST_RV32STC'

class Case_shape(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, rs1, rs1_data, rs1_shape ):
        return f'VECVT_M_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]}, 0, 0 )'
class Case_stride(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, rs1, stride_rd, stride_s1, rs1_data, rs1_shape ):
        return f'VECVT_M_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_rd}, {stride_s1} )'
class Case_rs1_internal(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, rs1, rs1_data, rs1_shape ):
        return f'VEXX_XX_M_INPLACE_RS1_INTERNAL( {num}, {name}, {rd}, {rs1_data}, {rs1_shape[0]}, {rs1_shape[1]} )'
class Case_misaligned_base(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, height, width, doff, soff1 ):
        return f'TEST_VEXX_XX_M_MISALIGNED_BASE( {num}, {name}, {height}, {width}, {doff}, {soff1} )'
class Case_misaligned_stride(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, height, width, dstride, sstride1 ):
        return f'TEST_VEXX_XX_M_MISALIGNED_STRIDE( {num}, {name}, {height}, {width}, {dstride}, {sstride1} )'
class Case_invalid_param(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, height, width ):
        return f'TEST_VEXX_XX_M_INVALID_PARAM( {num}, {name}, {height}, {width} )'
class Case_access_fault(BaseCase_VEXX_XX_M):
    def template( self, num, name, rd, dst, src1, height, width ):
        return f'TEST_VEXX_XX_M_ACCESS_FAULT( {num}, {name}, {dst}, {src1}, {height}, {width} )'

class BaseTest_vexx_xx_m(BaseTest):
    start = -128
    stop = 127
    stype = np.half

    @pytest.mark.parametrize( 'height, width', [
        #************************************************
        # Test shapes
        #************************************************/
        # Functional tests with basic data */
        [ 6, 8 ],
        [ 64, 64 ],
        [ 128, 128 ],
        [ 256, 256 ],
        [ 512, 256 ],
        # near 64 mac */ 
        [ 31, 63 ],
        [ 33, 65 ],
        [ 33, 63 ],

        # small shapes */
        [ 1, 1 ],
        [ 1, 10 ],
        [ 10, 1 ],
        [ 10, 10 ],
        # middle shape */ 
        [ 127, 127 ],
        [ 127, 255 ],
        [ 255, 127 ],
        [ 255, 255 ],


        # full of l1buffer */
        [ 40960, 8 ],
        [ 853, 256 ],
        [ 256, 853 ],

        # Functional tests with special float */
        #special_float_xx_m( stype, 5, 2) 
    ] )
    def test_shape( self, height, width ):
        rs1 = linspace_xx_m( self.start, self.stop, self.stype, height, width )
        simulate( self, self.Case_shape_inst, rs1=rs1 )
    
    @pytest.mark.parametrize( 'height, width, stride_rd, stride_s1', [
        # Functional tests for stride */
        [ 32, 64, 128, 0 ],
        [ 32, 64,  0, 128 ],
        [ 32, 64, 128, 128 ],
        [ 32, 63, 130, 130 ],
        [ 32, 65, 254, 254 ],
        [ 32, 63, 126, 126 ],

        #row=1, rs and rd stride < width test
        [ 1, 63, 31, 31 ],
    ] )
    def test_stride( self, height, width, stride_rd, stride_s1 ):
        [ rs1, stride_rd, stride_s1 ] = linspace_xx_m_stride( self.start, self.stop, self.stype, height, width, stride_rd, stride_s1 )
        simulate( self, self.Case_stride_inst, rs1=rs1, stride_rd=stride_rd, stride_s1=stride_s1 )

    @pytest.mark.parametrize( 'height, width', [
        #*****************************************************
        #Test rd and rs with same base address
        #******************************************************/
        [ 4, 4 ]      
    ] )
    def test_rs1_internal( self, height, width ):
        rs1 = linspace_xx_m( self.start, self.stop, self.stype, height, width )
        simulate( self, self.Case_rs1_internal_inst, rs1=rs1 )

    @pytest.mark.parametrize( 'height, width, doff, soff1', [
        #*****************************************************
        #Exception test with misaligned base addr
        #******************************************************/
        #rs misaligned
        [ 2, 2, 1, 0 ],
        #rs misaligned
        [ 2, 2, 0, 1 ],
        #rs and rd misaligned
        [ 2, 2, 3, 3 ],
    ] )
    def test_misaligned_base( self, height, width, doff, soff1 ):
        simulate( self, self.Case_misaligned_base_inst, height=height, width=width, doff=doff, soff1=soff1 )

    @pytest.mark.parametrize( 'height, width, dstride, sstride1', [
        #*****************************************************
        #Exception test with misaligned stride
        #******************************************************/
        #rd  stride misaligned 
        [ 32, 32, 67, 0 ],
        #rs stride misaligned
        [ 32, 32, 0, 67 ],
        #rs and rd stride misaligned
        [ 32, 32, 67, 67 ],
    ] )
    def test_misaligned_stride( self, height, width, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, dstride=dstride, sstride1=sstride1 )

    @pytest.mark.parametrize( 'height, width', [
        #*****************************************************
        #Exception test with invalid params
        #******************************************************/
        #height=0
        [ 0, 32 ],
        #width=0
        [ 32, 0 ],
        #height=width=0
        [ 0, 0 ],
    ] )
    def test_invalid_param( self, height, width ):
        simulate( self, self.Case_invalid_param_inst, height=height, width=width )

    @pytest.mark.parametrize( 'dst, src1, height, width', [
        #*****************************************************
        #Exception test with access fault
        #******************************************************/
        #rd in ddr 1k
        [ 0x400, 'VECAT_RS_ADDR', 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 0xbffffffc, 'VECAT_RS_ADDR', 32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 0xc013fffc, 'VECAT_RS_ADDR', 12, 24 ],
        #rd span from reserved to IB，0xc0400000 - 4 = 0xc03ffffc
        [ 0xc03ffffc, 'VECAT_RS_ADDR', 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0xc043fffc, 'VECAT_RS_ADDR', 32, 32 ],

        #rs1 in ddr 1k
        [ 'VECAT_RD_ADDR', 0x400, 24, 24 ],
        #rs1 span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VECAT_RD_ADDR', 0xbffffffc,  32, 32 ],
        #rs1 span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VECAT_RD_ADDR', 0xc013fffc, 12, 24 ],
        #rs1 span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VECAT_RD_ADDR', 0xc03ffffc, 32, 32 ],
        #rs1 span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VECAT_RD_ADDR', 0xc043fffc, 32, 32 ],
    ] )
    def test_access_fault( self, dst, src1, height, width ):
        simulate( self, self.Case_access_fault_inst, dst=dst, src1=src1, height=height, width=width )
    

class Test_vecvt_hf_x8_m(BaseTest_vexx_xx_m):
    inst = Vecvt_hf_x8_m
    start = -128
    stop = 127
    stype = np.int8
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'

    def test_rs1_internal(self):
        pass

    @pytest.mark.parametrize( 'height, width, doff, soff1', [
        #*****************************************************
        #Exception test with misaligned base addr
        #******************************************************/
        #rd 2 byte aligned, rs 1byte aligned
        [ 2, 2, 1, 0 ],
    ] )
    def test_misaligned_base( self, height, width, doff, soff1 ):
        simulate( self, self.Case_misaligned_base_inst, height=height, width=width, doff=doff, soff1=soff1 )

    @pytest.mark.parametrize( 'height, width, dstride, sstride1', [
        #*****************************************************
        #Exception test with misaligned stride
        #******************************************************/
        #rd  2x, rs 1x
        [ 32, 32, 67, 0 ],
    ] )
    def test_misaligned_stride( self, height, width, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, dstride=dstride, sstride1=sstride1 )    




class Test_vecvt_hf_xu8_m(BaseTest_vexx_xx_m):
    inst = Vecvt_hf_xu8_m
    start = 0
    stop = 255
    stype = np.uint8
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_HF_X8_M\n#include "vexx_xx_m.h"'

    def test_rs1_internal(self):
        pass

    @pytest.mark.parametrize( 'height, width, doff, soff1', [
        #*****************************************************
        #Exception test with misaligned base addr
        #******************************************************/
        #rd 2 byte aligned, rs 1byte aligned
        [ 2, 2, 1, 0 ],
    ] )
    def test_misaligned_base( self, height, width, doff, soff1 ):
        simulate( self, self.Case_misaligned_base_inst, height=height, width=width, doff=doff, soff1=soff1 )

    @pytest.mark.parametrize( 'height, width, dstride, sstride1', [
        #*****************************************************
        #Exception test with misaligned stride
        #******************************************************/
        #rd  2x, rs 1x
        [ 32, 32, 67, 0 ],
    ] )
    def test_misaligned_stride( self, height, width, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, dstride=dstride, sstride1=sstride1 )  



class Test_vecvt_x8_hf_m(BaseTest_vexx_xx_m):
    inst = Vecvt_x8_hf_m
    start = -128
    stop = 127
    stype = np.half
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_X8_HF_M\n#include "vexx_xx_m.h"'

    @pytest.mark.parametrize( 'height, width, doff, soff1', [
        #*****************************************************
        #Exception test with misaligned base addr
        #******************************************************/
        #rd 1 byte aligned, rs 2 byteS aligned
        [ 2, 2, 0, 3 ],
    ] )
    def test_misaligned_base( self, height, width, doff, soff1 ):
        simulate( self, self.Case_misaligned_base_inst, height=height, width=width, doff=doff, soff1=soff1 )

    @pytest.mark.parametrize( 'height, width, dstride, sstride1', [
        #*****************************************************
        #Exception test with misaligned stride
        #******************************************************/
        #rd  1x, rs 2x
        [ 32, 32, 0, 67 ],
    ] )
    def test_misaligned_stride( self, height, width, dstride, sstride1 ):
        simulate( self, self.Case_misaligned_stride_inst, height=height, width=width, dstride=dstride, sstride1=sstride1 ) 

class Test_veexp_m(BaseTest_vexx_xx_m):
    inst = Veexp_m
    start = -1.0
    stop = 1
    stype = np.half
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'

class Test_vesqrt_m(BaseTest_vexx_xx_m):
    inst = Vesqrt_m
    start = -20
    stop = 20
    stype = np.half
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'

class Test_verecip_m(BaseTest_vexx_xx_m):
    inst = Verecip_m
    start = -20
    stop = 20
    stype = np.half
    

    class Case_shape_inst(Case_shape):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_stride_inst(Case_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_rs1_internal_inst(Case_rs1_internal):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_base_inst(Case_misaligned_base):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_misaligned_stride_inst(Case_misaligned_stride):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_invalid_param_inst(Case_invalid_param):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'
    class Case_access_fault_inst(Case_access_fault):
        head = '#define VEXX_M_DEFAULT\n#include "vexx_xx_m.h"'