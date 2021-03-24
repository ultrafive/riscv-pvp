import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fsqrt import *


class BaseCase_rvf_compute_op1(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    footer = ''

class Case_fp_op1_s(BaseCase_rvf_compute_op1):
    def template( self, num, name, res, rs1, flag ):
        return f'TEST_FP_OP1_S( {num}, {name}, {flag}, {res}, {rs1} );'

class Case_fp_op1_s_dword_result(BaseCase_rvf_compute_op1):
    def template( self, num, name, res, rs1, flag ):
        return f'TEST_FP_OP1_S_DWORD_RESULT( {num}, {name}, {flag}, {res}, {rs1} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_compute_op1(BaseTest):

    def test_arithmetic(self, rs1, flag):
        simulate(self, Case_fp_op1_s, rs1=rs1, flag=flag)

    def test_dword_result(self, rs1, flag):
        simulate(self, Case_fp_op1_s_dword_result, rs1=rs1, flag=flag)

        
class Test_fsqrt(BaseTest_rvf_compute_op1):
    inst = Fsqrt
    argnames = { 'test_arithmetic': ['rs1', 'flag' ],
    'test_dword_result': ['rs1', 'flag'] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 3.14159265, 1 ],
        [      10000, 0 ],
        [        171, 1 ],

    ]
    param_dword_result = [
        [ -1.0, 0x10 ]
    ]
    params = { 'test_arithmetic': param_arithmetic, 
    'test_dword_result': param_dword_result }


