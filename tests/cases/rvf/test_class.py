import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.fclass import *


class BaseCase_rvf_class(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = ''
    footer = ''

class Case_fclass_s(BaseCase_rvf_class):
    def template( self, num, name, res, correct, input ):
        return f'TEST_FCLASS_S( {num}, {correct}, {input} );'


def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvf_fclass_s(BaseTest):

    def test_fclass_s(self, correct, input):
        simulate(self, Case_fclass_s, correct=correct, input=input)


        
class Test_fclass(BaseTest_rvf_fclass_s):
    inst = Fclass
    argnames = { 'test_fclass_s': ['correct', 'input' ] }
    param_fclass_s = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ 1 << 0, 0xff800000 ],
        [ 1 << 1, 0xbf800000 ],
        [ 1 << 2, 0x807fffff ],
        [ 1 << 3, 0x80000000 ],
        [ 1 << 4, 0x00000000 ],
        [ 1 << 5, 0x007fffff ],
        [ 1 << 6, 0x3f800000 ],
        [ 1 << 7, 0x7f800000 ],
        [ 1 << 8, 0x7f800001 ],
        [ 1 << 9, 0x7fc00000 ],

    ]

    params = { 'test_fclass_s': param_fclass_s }


