import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.feq import *
from isa.rvf.fle import *
from isa.rvf.flt import *


class BaseCase_rvf_cmp(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    foot = ''

class Case_cmp(BaseCase_rvf_cmp):
    def template( self, num, name, res, rs1, rs2, flags ):
        return f'TEST_FP_CMP_OP_S( {num}, {name}, {flags}, {res}, {rs1}, {rs2} );'


def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_cmp(BaseTest):

    def test_cmp(self, rs1, rs2, flags):
        simulate(self, Case_cmp, rs1=rs1, rs2=rs2, flags=flags)


        
class Test_feq(BaseTest_rvf_cmp):
    inst = Feq
    argnames = { 'test_cmp': ['rs1', 'rs2', 'flags' ] }
    param_cmp = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ -1.36, -1.36, 0x00 ],
        [ -1.37, -1.36, 0x00 ],
        [ 'NaN',     0, 0x00 ],
        [ 'NaN', 'NaN', 0x00 ],        
        # Skip this for LLVM because LLVM mc does not recognize
        # binary float directives like
        #   .float 0f:7fc00000
        # in expansion of sNaNf.
        #ifndef __clang__
        #[ sNaNf,     0, 0x10 ],
        #endif
    ]

    params = { 'test_cmp': param_cmp }

class Test_fle(BaseTest_rvf_cmp):
    inst = Fle
    argnames = { 'test_cmp': ['rs1', 'rs2', 'flags' ] }
    param_cmp = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ -1.36, -1.36, 0x00 ],
        [ -1.37, -1.36, 0x00 ],
        [ 'NaN',     0, 0x10 ],
        [ 'NaN', 'NaN', 0x10 ],        
        # Skip this for LLVM because LLVM mc does not recognize
        # binary float directives like
        #   .float 0f:7fc00000
        # in expansion of sNaNf.
        #ifndef __clang__
        #[ sNaNf,     0, 0x10 ],
        #endif
    ]

    params = { 'test_cmp': param_cmp }

class Test_flt(BaseTest_rvf_cmp):
    inst = Flt
    argnames = { 'test_cmp': ['rs1', 'rs2', 'flags' ] }
    param_cmp = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ -1.36, -1.36, 0x00 ],
        [ -1.37, -1.36, 0x00 ],
        [ 'NaN',     0, 0x10 ],
        [ 'NaN', 'NaN', 0x10 ],        
        # Skip this for LLVM because LLVM mc does not recognize
        # binary float directives like
        #   .float 0f:7fc00000
        # in expansion of sNaNf.
        #ifndef __clang__
        #[ sNaNf,     0, 0x10 ],
        #endif
    ]

    params = { 'test_cmp': param_cmp }


