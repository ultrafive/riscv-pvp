import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fsgnj import *
from isa.rvf.fsgnjn import *
from isa.rvf.fsgnjx import *

class BaseCase_move(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    foot = ''

class Case_macro(BaseCase_move):
    def template( self, num, name, rd, macro ):
        return f'{macro}'
class Case_fsgnjs(BaseCase_move):
    def template( self, num, name, rd, rs1_sign, rs2_sign):
        return f'TEST_FSGNJS({num}, {name}, {rd}, {rs1_sign}, {rs2_sign})'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len(params):
        metafunc.parametrize(
            argnames, [ param for param in params ]
        )

class BaseTest_move(BaseTest):

    def test_macro(self, macro):
        if macro != 0:
            simulate( self, Case_macro, macro=macro )

    def test_fsgnjs(self, rs1_sign, rs2_sign):
        simulate( self, Case_fsgnjs, rs1_sign=rs1_sign, rs2_sign=rs2_sign )


class Test_fsgnj(BaseTest_move):
    inst = Fsgnj
    argnames = { 'test_macro': ['macro'], 
    'test_fsgnjs': [ 'rs1_sign', 'rs2_sign' ] }
    param_macro = [
        [ '''
  TEST_CASE(2, a1, 1, csrwi fcsr, 1; li a0, 0x1234; fssr a1, a0)
  TEST_CASE(3, a0, 0x34, frsr a0)
  TEST_CASE(4, a0, 0x14, frflags a0)
  TEST_CASE(5, a0, 0x01, csrrwi a0, frm, 2)
  TEST_CASE(6, a0, 0x54, frsr a0)
  TEST_CASE(7, a0, 0x14, csrrci a0, fflags, 4)
  TEST_CASE(8, a0, 0x50, frsr a0)
        ''' ]
    ]
    param_fsgnjs = [
        [ 0, 0 ],
        [ 0, 1 ],
        [ 1, 0 ],
        [ 1, 1 ],
    ]
    params = { 'test_macro': param_macro,
    'test_fsgnjs': param_fsgnjs }

class Test_fsgnjn(BaseTest_move):
    inst = Fsgnjn
    argnames = { 'test_macro': ['macro'], 
    'test_fsgnjs': [ 'rs1_sign', 'rs2_sign' ] }
    param_macro = [ [0] ]
    param_fsgnjs = [
        [ 0, 0 ],
        [ 0, 1 ],
        [ 1, 0 ],
        [ 1, 1 ],
    ]
    params = { 'test_macro': param_macro,
    'test_fsgnjs': param_fsgnjs }

class Test_fsgnjx(BaseTest_move):
    inst = Fsgnjx
    argnames = { 'test_macro': ['macro'], 
    'test_fsgnjs': [ 'rs1_sign', 'rs2_sign' ] }
    param_macro = [ [0] ]
    param_fsgnjs = [
        [ 0, 0 ],
        [ 0, 1 ],
        [ 1, 0 ],
        [ 1, 1 ],
    ]
    params = { 'test_macro': param_macro,
    'test_fsgnjs': param_fsgnjs }

