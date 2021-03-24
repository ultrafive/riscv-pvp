import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.flw import *
from isa.rvf.fsw import *

class BaseCase_ldst(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = '''
tdat:
.word 0xbf800000
.word 0x40000000
.word 0x40400000
.word 0xc0800000
.word 0xdeadbeef
.word 0xcafebabe
.word 0xabad1dea
.word 0x1337d00d
'''
    footer = ''

class Case_case(BaseCase_ldst):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} )'


def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_ldst(BaseTest):

    def test_case(self, testreg, correctval, code):
        simulate( self, Case_case, testreg=testreg, correctval=correctval, code=code )


class Test_flw(BaseTest_ldst):
    inst = Flw
    argnames = { 'test_case': ['testreg', 'correctval', 'code'] }
    param_case = [
        [ 'a0', 0x40000000, 'la a1, tdat; flw f1, 4(a1); fsw f1, 20(a1); lw a0, 20(a1)' ]
    ]
    params = { 'test_case': param_case }

class Test_fsw(BaseTest_ldst):
    inst = Fsw
    argnames = { 'test_case': ['testreg', 'correctval', 'code'] }
    param_case = [
        [ 'a0', 0xbf800000, 'la a1, tdat; flw f1, 0(a1); fsw f1, 24(a1); lw a0, 24(a1)' ]
    ]
    params = { 'test_case': param_case }