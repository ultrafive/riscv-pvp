import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fmadd import *
from isa.rvf.fmsub import *
from isa.rvf.fnmadd import *
from isa.rvf.fnmsub import *



class BaseCase_rvf_fm(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    foot = ''

class Case_fp_op3_s(BaseCase_rvf_fm):
    def template( self, num, name, res, rs1, rs2, rs3, flags ):
        return f'TEST_FP_OP3_S( {num}, {name}, {flags}, {res}, {rs1}, {rs2}, {rs3} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_fm(BaseTest):

    def test_fp_op3_s(self, rs1, rs2, rs3, flags):
        simulate(self, Case_fp_op3_s, rs1=rs1, rs2=rs2, rs3=rs3, flags=flags)



class Test_fmadd(BaseTest_rvf_fm):
    inst = Fmadd
    argnames = { 'test_fp_op3_s': ['rs1', 'rs2', 'rs3', 'flags'] }
    param_fp_op3_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [   1.0,        2.5,        1.0,    0 ],
        [  -1.0,    -1235.1,        1.1,    1 ],
        [   2.0,       -5.0,       -2.0,    0 ],

    ]

    params = { 'test_fp_op3_s': param_fp_op3_s }

class Test_fmsub(BaseTest_rvf_fm):
    inst = Fmsub
    argnames = { 'test_fp_op3_s': ['rs1', 'rs2', 'rs3', 'flags'] }
    param_fp_op3_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [   1.0,        2.5,        1.0,    0 ],
        [  -1.0,    -1235.1,        1.1,    1 ],
        [   2.0,       -5.0,       -2.0,    0 ],

    ]

    params = { 'test_fp_op3_s': param_fp_op3_s }

class Test_fnmadd(BaseTest_rvf_fm):
    inst = Fnmadd
    argnames = { 'test_fp_op3_s': ['rs1', 'rs2', 'rs3', 'flags'] }
    param_fp_op3_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [   1.0,        2.5,        1.0,    0 ],
        [  -1.0,    -1235.1,        1.1,    1 ],
        [   2.0,       -5.0,       -2.0,    0 ],

    ]

    params = { 'test_fp_op3_s': param_fp_op3_s }

class Test_fnmsub(BaseTest_rvf_fm):
    inst = Fnmsub
    argnames = { 'test_fp_op3_s': ['rs1', 'rs2', 'rs3', 'flags'] }
    param_fp_op3_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [   1.0,        2.5,        1.0,    0 ],
        [  -1.0,    -1235.1,        1.1,    1 ],
        [   2.0,       -5.0,       -2.0,    0 ],

    ]

    params = { 'test_fp_op3_s': param_fp_op3_s }