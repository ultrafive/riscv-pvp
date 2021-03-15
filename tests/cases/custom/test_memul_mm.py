import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.memul_mm import *
from isa.custom.memul_hf_x8_mm import *

class BaseCase_METMUL_MM(BaseCase):
    head = '#include "memul.h"'


class Case_base(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]} )'
class Case_stride(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, stride_s1, stride_s2, stride_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL_STRIDE( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {stride_s1}, {stride_s2}, {stride_d} )'

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
        [ 4, 4, 4 ],
        [ 64, 64, 64 ],
        ]
    params_stride = [
        [ 64, 64, 64, 256, 0, 0 ],
        [ 64, 64, 64, 0, 256, 0 ],
    ]
    params = { 'test_base': params_base, 'test_stride': params_stride }    
    def test_base( self, vs1, vs2 ):
        simulate( self, self.Case_base_inst, vs1=vs1, vs2=vs2 )

    def test_stride( self, vs1, vs2, stride_s1, stride_s2, stride_d ):
        simulate( self, self.Case_stride_inst, vs1=vs1, vs2=vs2, stride_s1=stride_s1, stride_s2=stride_s2, stride_d=stride_d )

class Test_memul_mm(BaseTest_memul_mm):
    inst = Memul_mm
    lb = -1
    ub =  1
    data_function = { 'test_base':random_memul_mm, 'test_stride':random_memul_mm_stride }
    argnames = { 'test_base':[ 'vs1', 'vs2' ], 'test_stride':[ 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ] }

    class Case_base_inst(Case_base):
        head = '#define HF\n#include "memul.h"'
    class Case_stride_inst(Case_stride):
        head = '#define HF\n#include "memul.h"'

class Test_memul_hf_x8_mm(BaseTest_memul_mm):
    inst = Memul_hf_x8_mm
    lb = -128
    ub =  127
    data_function = { 'test_base':random_memul_hf_x8_mm, 'test_stride':random_memul_hf_x8_mm_stride }
    argnames = { 'test_base':[ 'dequant', 'vs1', 'vs2' ], 'test_stride':[ 'dequant', 'vs1', 'vs2', 'stride_s1', 'stride_s2', 'stride_d' ] }

    class Case_base_inst(Case_base):
        head = '#define HF_X8\n#include "memul.h"'
    class Case_stride_inst(Case_stride):
        head = '#define HF_X8\n#include "memul.h"'

    params = { 'test_base': params_base, 'test_stride': params_stride } 


    def test_base( self, dequant, vs1, vs2 ):
        simulate( self, self.Case_base_inst, dequant=dequant, vs1=vs1, vs2=vs2 )

    def test_stride( self, dequant, vs1, vs2, stride_s1, stride_s2, stride_d ):
        simulate( self, self.Case_stride_inst, dequant=dequant, vs1=vs1, vs2=vs2, stride_s1=stride_s1, stride_s2=stride_s2, stride_d=stride_d )


    def template( self, num, name, vd, vs1, vs2, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]} )'

class Case_stride(BaseCase_METMUL_MM):
    def template( self, num, name, vd, vs1, vs2, stride_s1, stride_s2, stride_d, vs1_data, vs1_shape, vs2_data, vs2_shape ):
        return f'TEST_MEMUL_STRIDE( {num}, {vd}, {vs1_data}, {vs2_data}, {vs1_shape[0]}, {vs1_shape[1]}, {vs2_shape[1]}, {stride_s1}, {stride_s2}, {stride_d} )'
