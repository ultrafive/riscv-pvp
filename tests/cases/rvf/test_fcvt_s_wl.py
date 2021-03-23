import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fcvt_s_w import *
from isa.rvf.fcvt_s_wu import *
from isa.rvf.fcvt_s_l import *
from isa.rvf.fcvt_s_lu import *


class BaseCase_rvf_cvt_s_wl(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    foot = ''

class Case_int_fp_op_s(BaseCase_rvf_cvt_s_wl):
    def template( self, num, name, res, val1 ):
        return f'TEST_INT_FP_OP_S( {num}, {name}, {res}, {val1} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_cvt_s_wl(BaseTest):

    def test_int_fp_op_s(self, val1):
        simulate(self, Case_int_fp_op_s, val1=val1)



class Test_fcvt_s_w(BaseTest_rvf_cvt_s_wl):
    inst = Fcvt_s_w
    argnames = { 'test_int_fp_op_s': ['val1'] }
    param_int_fp_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [  2 ],
        [ -2 ],

    ]

    params = { 'test_int_fp_op_s': param_int_fp_op_s }

class Test_fcvt_s_wu(BaseTest_rvf_cvt_s_wl):
    inst = Fcvt_s_wu
    argnames = { 'test_int_fp_op_s': ['val1'] }
    param_int_fp_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [  2 ],
        [ -2 ],

    ]

    params = { 'test_int_fp_op_s': param_int_fp_op_s }

'''

class Test_fcvt_s_l(BaseTest_rvf_cvt_s_wl):
    inst = Fcvt_s_l
    argnames = { 'test_int_fp_op_s': ['val1'] }
    param_int_fp_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        #if __riscv_xlen >= 64
        [  2 ],
        [ -2 ],
        # endif

    ]

    params = { 'test_int_fp_op_s': param_int_fp_op_s }

class Test_fcvt_s_lu(BaseTest_rvf_cvt_s_wl):
    inst = Fcvt_s_lu
    argnames = { 'test_int_fp_op_s': ['val1'] }
    param_int_fp_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        #if __riscv_xlen >= 64
        [  2 ],
        [ -2 ],
        #endif
    ]

    params = { 'test_int_fp_op_s': param_int_fp_op_s }

'''