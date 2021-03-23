import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.fence_i import *

class Case_fence_i(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = '''
insn:
  addi a3, a3, 333

2: addi a3, a3, 222
jalr a5, a6, 0

3: addi a3, a3, 555
jalr a5, a6, 0
'''
    foot = ''
    def template(self, num, name, rd, macro):
        return f'{macro}'

class Test_fence_i(BaseTest):
    inst = Fence_i
    @pytest.mark.parametrize( 'macro', [
        '''
li a3, 111
lh a0, insn
lh a1, insn+2

# test I$ hit
.align 6
sh a0, 2f, t0
sh a1, 2f+2, t0
fence.i

la a5, 2f
jalr a6, a5, 0
TEST_CASE( 2, a3, 444, nop )


# test prefetcher hit
li a4, 100
1: addi a4, a4, -1
bnez a4, 1b

sh a0, 3f, t0
sh a1, 3f+2, t0
fence.i

.align 6
la a5, 3f
jalr a6, a5, 0
TEST_CASE( 3, a3, 777, nop )
        '''
    ] )
    def test_fence_i(self, macro):
        simulate(self, Case_fence_i, macro=macro)
