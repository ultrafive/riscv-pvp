import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.lui import *
from isa.rvi.auipc import *

class BaseCase_rvi_uimm(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    footer = ''

class Case(BaseCase_rvi_uimm):
    def template(self, num, name, res, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} );'


def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_rvi_uimm(BaseTest):

    def test_case(self, testreg, correctval, code ):
        simulate(self, Case, testreg=testreg, correctval=correctval, code=code )
        
class Test_lui(BaseTest_rvi_uimm):
    inst = Lui
    argnames = { 'test_case': [ 'testreg', 'correctval', 'code' ],
    }
    param_case = [
        [ 'x1', 0x0000000000000000, 'lui x1, 0x00000' ],
        [ 'x1', 0xfffffffffffff800, 'lui x1, 0xfffff;sra x1,x1,1' ],
        [ 'x1', 0x00000000000007ff, 'lui x1, 0x7ffff;sra x1,x1,20' ],
        [ 'x1', 0xfffffffffffff800, 'lui x1, 0x80000;sra x1,x1,20' ],

        [ 'x0', 0, 'lui x0, 0x80000' ],
    ]
    params = { 'test_case': param_case }

class Test_auipc(BaseTest_rvi_uimm):
    inst = Auipc
    argnames = { 'test_case': [ 'testreg', 'correctval', 'code' ],
    }
    param_case = [
        [ 'a0', 10000, '.align 3;\nlla a0, 1f + 10000;\njal a1, 1f;\n1: sub a0, a0, a1;'],

        [ 'a0', -10000, '.align 3;\nlla a0, 1f - 10000;\njal a1, 1f;\n1: sub a0, a0, a1;'], 
    ]
    params = { 'test_case': param_case }
