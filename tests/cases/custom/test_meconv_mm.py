import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.meconv_mm import *

class BaseCase_MECONV_MM(BaseCase):
    header = '#define HF\n#include "meconv.h"'
    env = 'RVTEST_RV32STC'
    tdata = ''
    footer = ''

class Case_base(BaseCase_MECONV_MM):
    def template( self, num, name, vd, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl, vs1_data, vs1_shape, vs2_data, vs2_shape  ):
        return f'TEST_MECONV_PADDING_SK_DILATION( {num},  {vd}, {vs1_data}, {vs2_data}, {h}, {w}, {cin}, {cout}, {kh}, {kw}, OUT_H({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), OUT_W({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl} )'

class Case_stride(BaseCase_MECONV_MM):
    def template( self, num, name, vd, vs1, vs2, h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl, vs1_data, vs1_shape, vs2_data, vs2_shape  ):
        return f'TEST_MECONV_STRIDE( {num},  {vd}, {vs1_data}, {vs2_data}, {h}, {w}, {cin}, {cout}, {kh}, {kw}, OUT_H({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), OUT_W({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), {stride_s1}, {stride_s2}, {stride_d} )'

class Case_misaligned_block(BaseCase_MECONV_MM):
    def template( self, num, name, vd, vs1, vs2, h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl, vs1_data, vs1_shape, vs2_data, vs2_shape  ):
        return f'TEST_MECONV_MISALIGNED_BLOCK( {num},  {vd}, {vs1_data}, {vs2_data}, {h}, {w}, {cin}, {cout}, {kh}, {kw}, OUT_H({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), OUT_W({h}, {w}, {kh}, {kw}, {padding[0]}, {padding[1]}, {padding[2]}, {padding[3]}, {sk}, {dl}), {off_s1}, {off_s2}, {off_d} )'


class BaseTest_meconv_mm(BaseTest):

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl', [
        #*****************************#
        #*      Sanity tests         *#
        #*****************************#
        # Small case (1, 4, 4, 4) x (3, 3, 4, 4) = (1, 2, 2, 4)
        random_meconv_mm( 4, 4, 4, 4, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # Medium case (1, 16, 16, 16) x (5, 5, 16, 16) = (1, 12, 12, 16)
        random_meconv_mm( 16, 16, 16, 16, 5, 5, [ 0, 0, 0, 0 ], 1, 1 ),
        #ifdef FULL_TEST
        # Large case (1, 64, 64, 64) x (7, 7, 64, 32) = (1, 58, 58, 32)
        random_meconv_mm( 64, 64, 64, 32, 7, 7, [ 0, 0, 0, 0 ], 1, 1 ),
        #endif

        #*****************************#
        #*  Test input#filter shapes *#
        #*****************************#
        # Test height#width = 1
        # (1, 1, 1, 64) x (1, 1, 64, 64) = (1, 1, 1, 64)
        random_meconv_mm( 1, 1, 64, 64, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 1, 1024, 64) x (1, 1, 64, 64) = (1, 1, 1024, 64)
        random_meconv_mm( 1, 1024, 64, 64, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 1024, 1, 64) x (1, 1, 64, 64) = (1, 1024, 1, 64)
        random_meconv_mm( 1024, 1, 64, 64, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),

        #ifdef FULL_TEST
        # Test large height#width
        # (1, 512, 256, 2)[512k] x (1, 1, 2, 1) = (1, 512, 256, 1)[256k]
        random_meconv_mm( 512, 256, 2, 1, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 65535, 2, 2)[512k] x (1, 1, 2, 1) = (1, 65535, 2, 1)[256k]
        random_meconv_mm( 65535, 2, 2, 1, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 2, 65535, 2)[512k] x (1, 1, 2, 1) = (1, 2, 65535, 1)[256k]
        random_meconv_mm( 2, 65535, 2, 1, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),

        # Test random height#width
        # (1, 241, 415, 2) x (3, 3, 2, 1) = (1, 239, 413, 1)
        random_meconv_mm( 241, 415, 2, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 322, 147, 2) x (3, 3, 2, 1) = (1, 320, 145, 1)
        random_meconv_mm( 322, 147, 2, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 132, 95, 2) x (3, 3, 2, 1) = (1, 130, 93, 1)
        random_meconv_mm( 132, 95, 2, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 42, 77, 2) x (3, 3, 2, 1) = (1, 40, 75, 1)
        random_meconv_mm( 42, 77, 2, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        #endif

        # Test cin#cout = 1
        # (1, 128, 128, 1) x (3, 3, 1, 1) = (1, 126, 126, 1)
        random_meconv_mm( 128, 128, 1, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 32, 32, 1) x (3, 3, 1, 64) = (1, 30, 30, 64)
        random_meconv_mm( 32, 32, 1, 64, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 32, 32, 64) x (3, 3, 64, 1) = (1, 30, 30, 1)
        random_meconv_mm( 32, 32, 64, 1, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 1, 1, 1) x (1, 1, 1, 1) = (1, 1, 1, 1)
        random_meconv_mm( 1, 1, 1, 1, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),

        #ifdef FULL_TEST
        # Test large cin#cout
        # (1, 2, 2, 65535)[512k] x (1, 1, 65535, 1) = (1, 2, 2, 1)
        random_meconv_mm( 2, 2, 65535, 1, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 1, 2, 1) x (1, 1, 1, 65535) = (1, 1, 2, 65535)[256k]
        random_meconv_mm( 1, 2, 1, 65535, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 1, 1, 512) x (1, 1, 512, 512)[512k] = (1, 1, 1, 512)
        random_meconv_mm( 1, 1, 512, 512, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        #endif

        # Test random cin#cout
        # (1, 4, 4, 53) x (3, 3, 53, 152) = (1, 2, 2, 152)
        random_meconv_mm( 4, 4, 53, 152, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 4, 4, 149) x (3, 3, 149, 42) = (1, 2, 2, 42)
        random_meconv_mm( 4, 4, 149, 42, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 4, 4, 234) x (1, 1, 234, 193) = (1, 4, 4, 193)
        random_meconv_mm( 4, 4, 234, 193, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 8, 8, 17) x (1, 1, 17, 29) = (1, 4, 4, 29)
        random_meconv_mm( 8, 8, 17, 29, 5, 5, [ 0, 0, 0, 0 ], 1, 1 ),

        # Test filter shapes
        # (1, 64, 64, 16) x (1, 1, 16, 16) = (1, 64, 64, 16)
        random_meconv_mm( 64, 64, 16, 16, 1, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (1, 2, 16, 16) = (1, 64, 63, 16)
        random_meconv_mm( 64, 64, 16, 16, 1, 2, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (2, 1, 16, 16) = (1, 63, 64, 16)
        random_meconv_mm( 64, 64, 16, 16, 2, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (2, 2, 16, 16) = (1, 63, 63, 16)
        random_meconv_mm( 64, 64, 16, 16, 2, 2, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (3, 3, 16, 16) = (1, 62, 62, 16)
        random_meconv_mm( 64, 64, 16, 16, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (5, 5, 16, 16) = (1, 60, 60, 16)
        random_meconv_mm( 64, 64, 16, 16, 5, 5, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (7, 7, 16, 16) = (1, 58, 58, 16)
        random_meconv_mm( 64, 64, 16, 16, 7, 7, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (11, 11, 16, 16) = (1, 54, 54, 16)
        random_meconv_mm( 64, 64, 16, 16, 11, 11, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (3, 7, 16, 16) = (1, 62, 58, 16)
        random_meconv_mm( 64, 64, 16, 16, 3, 7, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (8, 4, 16, 16) = (1, 57, 61, 16)
        random_meconv_mm( 64, 64, 16, 16, 8, 4, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (1, 11, 16, 16) = (1, 64, 54, 16)
        random_meconv_mm( 64, 64, 16, 16, 1, 11, [ 0, 0, 0, 0 ], 1, 1 ),
        # (1, 64, 64, 16) x (11, 1, 16, 16) = (1, 54, 64, 16)
        random_meconv_mm( 64, 64, 16, 16, 11, 1, [ 0, 0, 0, 0 ], 1, 1 ),

        # Test some random shapes
        random_meconv_mm( 52, 7, 21, 41, 3, 6, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 58, 14, 9, 51, 2, 9, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 95, 35, 62, 11, 8, 8, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 82, 57, 3, 21, 5, 1, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 19, 35, 45, 23, 6, 2, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 25, 62, 15, 48, 3, 9, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 72, 51, 45, 32, 5, 5, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 74, 21, 34, 31, 5, 4, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 60, 47, 10, 42, 3, 5, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 10, 42, 28, 34, 7, 2, [ 0, 0, 0, 0 ], 1, 1 ),

        # Test blocking edge cases
        random_meconv_mm( 63, 65, 4, 4, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
        random_meconv_mm( 65, 63, 4, 4, 3, 3, [ 0, 0, 0, 0 ], 1, 1 ),
    ] )
    def test_base( self, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl ):
        simulate( self, Case_base, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl', [
        #*****************************/
        #*       Test paddings       */
        #*****************************/
        # Test padding = 'SAME'
        #   (1x1) input
        random_meconv_mm( 1, 1, 4, 4, 3, 3, [ 1, 1, 1, 1 ], 1, 1),
        random_meconv_mm( 1, 1, 4, 4, 5, 5, [ 2, 2, 2, 2 ], 1, 1),
        random_meconv_mm( 1, 1, 4, 4, 7, 7, [ 3, 3, 3, 3 ], 1, 1),
        random_meconv_mm( 1, 1, 4, 4, 15, 15, [ 7, 7, 7, 7 ], 1, 1),
        #   random size input
        random_meconv_mm( 24, 51, 4, 4, 5, 7, [ 2, 2, 3, 3 ], 1, 1),
        random_meconv_mm( 34, 14, 4, 4, 11, 13, [ 5, 5, 6, 6 ], 1, 1),

        # Test unparallel padding (pad_top != pad_bottom, pad_left != pad_right)
        random_meconv_mm( 14, 51, 4, 4, 5, 5, [ 2, 3, 1, 4 ], 1, 1),
        random_meconv_mm( 17, 12, 4, 4, 2, 6, [ 6, 3, 2, 5 ], 1, 1),

        # Test partial padding (pad_[top|bottom|left|right] = 0)
        random_meconv_mm( 16, 16, 4, 4, 5, 5, [ 0, 2, 0, 2 ], 1, 1),
        random_meconv_mm( 16, 16, 4, 4, 5, 5, [ 2, 0, 2, 0 ], 1, 1),
        random_meconv_mm( 16, 16, 4, 4, 5, 5, [ 0, 2, 2, 0 ], 1, 1),
        random_meconv_mm( 16, 16, 4, 4, 5, 5, [ 2, 0, 0, 2 ], 1, 1),

        #ifdef FULL_TEST
        # Test large padding
        random_meconv_mm( 2, 2, 2, 2, 2, 2, [ 100, 100, 100, 100 ], 1, 1),
        random_meconv_mm( 2, 2, 2, 2, 2, 2, [ 255, 255, 0, 0 ], 1, 1),
        #endif
    ] )
    def test_paddings( self, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl ):
        simulate( self, Case_base, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl', [
        #*****************************/
        #*   Test conv stride (s_k)  */
        #*****************************/
        # Regular cases
        #   with padding
        random_meconv_mm( 64, 64, 4, 4, 3, 3, [ 1, 1, 1, 1 ], 2, 1),
        #   without padding
        random_meconv_mm( 64, 64, 4, 4, 5, 5, [ 0, 0, 0, 0 ], 4, 1),

        # Test SK > kh/kw
        random_meconv_mm( 16, 16, 4, 4, 5, 5, [ 2, 2, 2, 2 ], 8, 1),

        # Test SK > h/w
        random_meconv_mm( 16, 16, 4, 4, 3, 3, [ 1, 1, 1, 1 ], 32, 1),

        #ifdef FULL_TEST
        # Test large SK
        random_meconv_mm( 1024, 1, 4, 4, 3, 3, [ 1, 1, 1, 1 ], 255, 1),

        # Some random cases
        random_meconv_mm( 23, 41, 3, 4, 5, 7, [ 2, 3, 1, 0 ], 7, 1),
        random_meconv_mm( 37, 25, 4, 2, 4, 1, [ 6, 5, 7, 3 ], 9, 1),
        random_meconv_mm( 44, 51, 2, 2, 6, 3, [ 2, 1, 0, 7 ], 21, 1),
        #endif
    ] )
    def test_conv_stride( self, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl ):
        simulate( self, Case_base, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl', [
        #*****************************/
        #*       Test dilations      */
        #*****************************/
        # Regular cases
        #   without padding
        #ifndef SIM_GEM5
        random_meconv_mm( 64, 64, 4, 4, 3, 3, [ 0, 0, 0, 0 ], 2, 2),
        #   with padding = 'SAME'
        random_meconv_mm( 64, 64, 4, 4, 3, 3, [ 2, 2, 2, 2 ], 2, 2),

        # Test with kh = kw = 1
        random_meconv_mm( 64, 64, 4, 4, 1, 1, [ 0, 0, 0, 0 ], 1, 4),

        # Test dilation = SK
        random_meconv_mm( 80, 80, 2, 2, 3, 3, [ 0, 0, 0, 0 ], 7, 7),

        # Test dilation < SK
        random_meconv_mm( 63, 63, 2, 2, 3, 3, [ 0, 0, 0, 0 ], 5, 3),

        # Test output shape = (1, 1) with dilation
        random_meconv_mm( 15, 15, 4, 4, 3, 3, [ 0, 0, 0, 0 ], 1, 7),

        #ifdef FULL_TEST
        # Test large dilation
        random_meconv_mm( 1024, 256, 1, 1, 2, 2, [ 0, 0, 0, 0 ], 1, 255),

        # Test large dilation with large padding
        random_meconv_mm( 3, 3, 4, 4, 3, 3, [ 255, 255, 255, 255 ], 1, 255),

        # Some random cases
        random_meconv_mm( 124, 141, 2, 2, 3, 5, [ 12, 42, 32, 14 ], 3, 5),
        random_meconv_mm( 54, 91, 5, 3, 7, 3, [ 4, 3, 9, 11 ], 2, 2),
        random_meconv_mm( 71, 48, 2, 3, 4, 2, [ 3, 2, 2, 5 ], 3, 3),
        #endif
        #endif  !SIM_GEM5
    ] )
    def test_dilations( self, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl ):
        simulate( self, Case_base, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl', [
        #*****************************/
        #*       Stride tests        */
        #*****************************/
        # stride == cin/cout == 128
        random_meconv_mm_stride( 16, 16, 64, 64, 3, 3, 128, 128, 128, [ 0, 0, 0, 0 ], 1, 1),

        # Test input/filter/output stride combinations
        #   cin bytes = 128, input stride = 130
        random_meconv_mm_stride( 16, 16, 64, 1, 3, 3, 130, 0, 0, [ 0, 0, 0, 0 ], 1, 1),
        #   cout bytes = 126, filter stride = 128, output stride = 130
        random_meconv_mm_stride( 16, 16, 1, 63, 3, 3, 0, 128, 130, [ 0, 0, 0, 0 ], 1, 1),
        #   cin bytes = 2, cout bytes = 2,
        #   input stride = 12, filter stride = 24, output stride = 48
        random_meconv_mm_stride( 16, 16, 1, 1, 3, 3, 12, 24, 48, [ 0, 0, 0, 0 ], 1, 1),

        # Random cases
        random_meconv_mm_stride( 12, 15, 23, 14, 5, 2, 48, 54, 70, [ 0, 0, 0, 0 ], 1, 1),
        random_meconv_mm_stride( 21, 12, 13, 12, 3, 2, 52, 34, 78, [ 0, 0, 0, 0 ], 1, 1),
    ] )
    def random_meconv_mm_stride( self, vs1, vs2, h, w, cin, cout, kh, kw, stride_s1, stride_s2, stride_d, padding, sk, dl ):
        simulate( self, Case_stride, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, stride_s1=stride_s1, stride_s2=stride_s2, stride_d=stride_d, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl', [
        #**********************************************/
        #*        Misaligned address tests            */
        #* (2-byte aligned but not 128-byte aligned)  */
        #**********************************************/
        # Test misaligned RS1 address
        random_meconv_mm_misaligned_block( 64, 64, 4, 4, 3, 3, 12, 0, 0, [ 0, 0, 0, 0 ], 1, 1),
        # Test misaligned RS2 address
        random_meconv_mm_misaligned_block( 64, 64, 4, 4, 3, 3, 0, 14, 0, [ 0, 0, 0, 0 ], 1, 1),
        # Test misaligned RD address
        random_meconv_mm_misaligned_block( 64, 64, 4, 4, 3, 3, 0, 0, 16, [ 0, 0, 0, 0 ], 1, 1),
        # Test misaligned RS1/RS2/RD addresses
        random_meconv_mm_misaligned_block( 64, 64, 4, 4, 3, 3, 128, 52, 84, [ 0, 0, 0, 0 ], 1, 1),


    ] )
    def random_misaligned_block( self, vs1, vs2, h, w, cin, cout, kh, kw, off_s1, off_s2, off_d, padding, sk, dl ):
        simulate( self, Case_misaligned_block, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, off_s1=off_s1, off_s2=off_s2, off_d=off_d, padding=padding, sk=sk, dl=dl )

    @pytest.mark.parametrize( 'vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl', [
        #*****************************/
        #*   Special FP value tests  */
        #*****************************/
        meconv_mm_special_fp( 1, 10, 1, 10, 1, 1, [ 0, 0, 0, 0 ], 1, 1 )
    ] )
    def test_sepcial_fp( self, vs1, vs2, h, w, cin, cout, kh, kw, padding, sk, dl ):
        simulate( self, Case_base, vs1=vs1, vs2=vs2, h=h, w=w, cin=cin, cout=cout, kh=kh, kw=kw, padding=padding, sk=sk, dl=dl )

class Test_meconv_mm(BaseTest_meconv_mm):
    inst = Meconv_mm