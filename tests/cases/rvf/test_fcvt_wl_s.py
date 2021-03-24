import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fcvt_w_s import *
from isa.rvf.fcvt_wu_s import *
from isa.rvf.fcvt_l_s import *
from isa.rvf.fcvt_lu_s import *


class BaseCase_rvf_cvt_wl_s(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = '''
# -NaN, NaN, -inf, +inf
tdat:
.word 0xffffffff
.word 0x7fffffff
.word 0xff800000
.word 0x7f800000

tdat_d:
.dword 0xffffffffffffffff
.dword 0x7fffffffffffffff
.dword 0xfff0000000000000
.dword 0x7ff0000000000000
'''
    footer = ''

class Case_fp_int_op_s(BaseCase_rvf_cvt_wl_s):
    def template( self, num, name, res, val1, rm, flags ):
        return f'TEST_FP_INT_OP_S( {num}, {name}, {flags}, {res}, {val1}, {rm} );'

class Case_base(BaseCase_rvf_cvt_wl_s):
    def template( self, num, name, res, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_cvt_wl_s(BaseTest):

    def test_fp_int_op_s(self, val1, rm, flags):
        simulate(self, Case_fp_int_op_s, val1=val1, rm=rm, flags=flags)

    def test_case(self, testreg, correctval, code):
        simulate(self, Case_base, testreg=testreg, correctval=correctval, code=code)



class Test_fcvt_w_s(BaseTest_rvf_cvt_wl_s):
    inst = Fcvt_w_s
    argnames = { 'test_fp_int_op_s': ['val1', 'rm', 'flags' ],
    'test_case': ['testreg', 'correctval', 'code'] }
    param_fp_int_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ -1.1,  'rtz', 0x01 ],
        [ -1.0,  'rtz', 0x00 ],
        [ -0.9,  'rtz', 0x01 ],
        [  0.9,  'rtz', 0x01 ],
        [  1.0,  'rtz', 0x00 ],
        [  1.1,  'rtz', 0x01 ],
        [ -3e9,  'rtz', 0x10 ],
        [  3e9,  'rtz', 0x10 ],
    ]
    param_case = [
        # test negative NaN, negative infinity conversion
        [ 'x1', 0x000000007fffffff, 'la x1, tdat  ; flw f1,  0(x1); fcvt.w.s x1, f1'],
        [ 'x1', 0xffffffff80000000, 'la x1, tdat  ; flw f1,  8(x1); fcvt.w.s x1, f1'],
        # test positive NaN, positive infinity conversion
        [ 'x1', 0x000000007fffffff, 'la x1, tdat  ; flw f1,  4(x1); fcvt.w.s x1, f1'],
        [ 'x1', 0x000000007fffffff, 'la x1, tdat  ; flw f1, 12(x1); fcvt.w.s x1, f1'],
    ]

    params = { 'test_fp_int_op_s': param_fp_int_op_s,
    'test_case': param_case }

class Test_fcvt_wu_s(BaseTest_rvf_cvt_wl_s):
    inst = Fcvt_wu_s
    argnames = { 'test_fp_int_op_s': ['val1', 'rm', 'flags' ],
    'test_case': ['testreg', 'correctval', 'code'] }
    param_fp_int_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ -3.0,  'rtz', 0x10 ],
        [ -1.0,  'rtz', 0x10 ],
        [ -0.9,  'rtz', 0x01 ],
        [  0.9,  'rtz', 0x01 ],
        [  1.0,  'rtz', 0x00 ],
        [  1.1,  'rtz', 0x01 ],
        [ -3e9,  'rtz', 0x10 ],
        [  3e9,  'rtz', 0x00 ],
    ]
    param_case = [
        # test NaN, infinity conversions to unsigned integer
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1,  0(x1); fcvt.wu.s x1, f1' ],
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1,  4(x1); fcvt.wu.s x1, f1' ],
        [ 'x1',                  0, 'la x1, tdat  ; flw f1,  8(x1); fcvt.wu.s x1, f1' ],
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1, 12(x1); fcvt.wu.s x1, f1' ],
    ]

    params = { 'test_fp_int_op_s': param_fp_int_op_s,
    'test_case': param_case }

'''

class Test_fcvt_l_s(BaseTest_rvf_cvt_wl_s):
    inst = Fcvt_l_s
    argnames = { 'test_fp_int_op_s': ['val1', 'rm', 'flags' ],
    'test_case': ['testreg', 'correctval', 'code'] }
    param_fp_int_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        #if __riscv_xlen >= 64
        [ -1.1,  'rtz', 0x01 ],
        [ -1.0,  'rtz', 0x00 ],
        [ -0.9,  'rtz', 0x01 ],
        [  0.9,  'rtz', 0x01 ],
        [  1.0,  'rtz', 0x00 ],
        [  1.1,  'rtz', 0x01 ],
        #endif
    ]
    param_case = [
        # test negative NaN, negative infinity conversion
        #if __riscv_xlen >= 64
        [ 'x1', 0x7fffffffffffffff, 'la x1, tdat  ; flw f1,  0(x1); fcvt.l.s x1, f1'],
        [ 'x1', 0x8000000000000000, 'la x1, tdat  ; flw f1,  8(x1); fcvt.l.s x1, f1'],
        #endif
        # test positive NaN, positive infinity conversion
        #if __riscv_xlen >= 64
        [ 'x1', 0x7fffffffffffffff, 'la x1, tdat  ; flw f1,  4(x1); fcvt.l.s x1, f1'],
        [ 'x1', 0x7fffffffffffffff, 'la x1, tdat  ; flw f1, 12(x1); fcvt.l.s x1, f1'],
        #endif
    ]

    params = { 'test_fp_int_op_s': param_fp_int_op_s,
    'test_case': param_case }

class Test_fcvt_lu_s(BaseTest_rvf_cvt_wl_s):
    inst = Fcvt_lu_s
    argnames = { 'test_fp_int_op_s': ['val1', 'rm', 'flags' ],
    'test_case': ['testreg', 'correctval', 'code'] }
    param_fp_int_op_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        #if __riscv_xlen >= 64
        [ -3.0,  'rtz', 0x10 ],
        [ -1.0,  'rtz', 0x10 ],
        [ -0.9,  'rtz', 0x01 ],
        [  0.9,  'rtz', 0x01 ],
        [  1.0,  'rtz', 0x00 ],
        [  1.1,  'rtz', 0x01 ],
        [ -3e9,  'rtz', 0x10 ],
        #endif
    ]
    param_case = [
        # test NaN, infinity conversions to unsigned integer
        #if __riscv_xlen >= 64
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1,  0(x1); fcvt.lu.s x1, f1' ],
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1,  4(x1); fcvt.lu.s x1, f1' ],
        [ 'x1',                  0, 'la x1, tdat  ; flw f1,  8(x1); fcvt.lu.s x1, f1' ],
        [ 'x1', 0xffffffffffffffff, 'la x1, tdat  ; flw f1, 12(x1); fcvt.lu.s x1, f1' ],
        #endif
    ]

    params = { 'test_fp_int_op_s': param_fp_int_op_s,
    'test_case': param_case }
'''