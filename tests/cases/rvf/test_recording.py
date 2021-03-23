import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvf.flw import *

class BaseCase_recording(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32UF'
    tdata = '''
minf: .float -Inf
three: .float 3.0
    '''
    foot = ''

class Case_macro(BaseCase_recording):
    def template( self, num, name, rd, macro ):
        return macro

class Test_recording(BaseTest):
    inst = Flw
    @pytest.mark.parametrize( 'macro', [
        '''
  # Make sure infinities with different mantissas compare as equal.
  flw f0, minf, a0
  flw f1, three, a0
  fmul.s f1, f1, f0
  TEST_CASE( 2, a0, 1, feq.s a0, f0, f1)
  TEST_CASE( 3, a0, 1, fle.s a0, f0, f1)
  TEST_CASE( 4, a0, 0, flt.s a0, f0, f1)
        ''' ,
         '''
  # Likewise, but for zeroes.
  fcvt.s.w f0, x0
  li a0, 1
  fcvt.s.w f1, a0
  fmul.s f1, f1, f0
  TEST_CASE(5, a0, 1, feq.s a0, f0, f1)
  TEST_CASE(6, a0, 1, fle.s a0, f0, f1)
  TEST_CASE(7, a0, 0, flt.s a0, f0, f1)
        ''' 
    ] )
    def test_macro(self, macro):
        simulate( self, Case_macro, macro=macro )



