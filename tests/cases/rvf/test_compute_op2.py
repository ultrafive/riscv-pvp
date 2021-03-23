import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fadd import *
from isa.rvf.fsub import *
from isa.rvf.fmul import *
from isa.rvf.fdiv import *
from isa.rvf.fmin import *
from isa.rvf.fmax import *

class BaseCase_rvf_compute_op2(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    foot = ''

class Case_fp_op2_s(BaseCase_rvf_compute_op2):
    def template( self, num, name, res, rs1, rs2, flag ):
        return f'TEST_FP_OP2_S( {num}, {name}, {flag}, {res}, {rs1}, {rs2} );'



def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_compute_op2(BaseTest):

    def test_arithmetic(self, rs1, rs2, flag):
        simulate(self, Case_fp_op2_s, rs1=rs1, rs2=rs2, flag=flag)

        
class Test_fadd(BaseTest_rvf_compute_op2):
    inst = Fadd
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [        2.5,        1.0, 0 ],
        [    -1235.1,        1.1, 1 ],
        [ 3.14159265, 0.00000001, 1 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }

class Test_fsub(BaseTest_rvf_compute_op2):
    inst = Fsub
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [        2.5,        1.0, 0 ],
        [    -1235.1,       -1.1, 1 ],
        [ 3.14159265, 0.00000001, 1 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }

class Test_fmul(BaseTest_rvf_compute_op2):
    inst = Fmul
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [        2.5,        1.0, 0 ],
        [    -1235.1,       -1.1, 1 ],
        [ 3.14159265, 0.00000001, 1 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }

class Test_fdiv(BaseTest_rvf_compute_op2):
    inst = Fdiv
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 3.14159265, 2.71828182, 1 ],
        [      -1234,     1235.1, 1 ],
        [ 3.14159265,        1.0, 0 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }

class Test_fmin(BaseTest_rvf_compute_op2):
    inst = Fmin
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [        2.5,        1.0,       0 ],
        [    -1235.1,        1.1,       0 ],
        [        1.1,    -1235.1,       0 ],
        [      'NaN',    -1235.1,       0 ],
        [ 3.14159265, 0.00000001,       0 ],
        [       -1.0,       -2.0,       0 ],
        # -0.0 < +0.0
        [       -0.0,        0.0,       0 ],
        [        0.0,       -0.0,       0 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }

class Test_fmax(BaseTest_rvf_compute_op2):
    inst = Fmax
    argnames = { 'test_arithmetic': ['rs1', 'rs2', 'flag' ] }
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [        2.5,        1.0,       0 ],
        [    -1235.1,        1.1,       0 ],
        [        1.1,    -1235.1,       0 ],
        [      'NaN',    -1235.1,       0 ],
        [ 3.14159265, 0.00000001,       0 ],
        [       -1.0,       -2.0,       0 ],
        # -0.0 < +0.0
        [       -0.0,        0.0,       0 ],
        [        0.0,       -0.0,       0 ],

    ]
    params = { 'test_arithmetic': param_arithmetic }