#
# This is the most basic self checking test. If your simulator does not
# pass thiss then there is little chance that it will pass any of the
# more complicated self checking tests.
#
import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.simple import *

class Case_simple(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    foot = ''

    def template( self, num, name, rd ):
        return f'RVTEST_PASS'

class Test_simple(BaseTest):
    inst = Simple

    def test_simple(self):
        simulate(self, Case_simple)
