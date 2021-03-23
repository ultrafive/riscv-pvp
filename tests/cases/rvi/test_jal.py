import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.jal import *
from isa.rvi.jalr import *

class BaseCase_jal(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    foot = ''

class Case_macro(BaseCase_jal):
    def template( self, num, name, rd, macro ):
        return macro
class Case_case(BaseCase_jal):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} )'

class Case_case_jalr(BaseCase_jal):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'.option push\n.align 2\n.option norvc\nTEST_CASE( {num}, {testreg}, {correctval}, {code} )\n.option pop'

class Case_src1_bypass(BaseCase_jal):
    def template( self, num, name, rd, nop_cycles ):
        return f'TEST_JR_SRC1_BYPASS( {num}, {nop_cycles}, {name} )'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_jal(BaseTest):

    def test_macro(self, macro):
        simulate( self, Case_macro, macro=macro )

    def test_case(self, testreg, correctval, code):
        simulate( self, Case_case, testreg=testreg, correctval=correctval, code=code )

class Test_jal(BaseTest_jal):
    inst = Jal
    argnames = { 'test_macro': ['macro'], 
    'test_case': ['testreg', 'correctval', 'code'],
    }
    param_macro = [
        #-------------------------------------------------------------
        # Test 2: Basic test
        #-------------------------------------------------------------
        ['''
        test_2:
        li  TESTNUM, 2
        li  ra, 0

        jal x4, target_2
        linkaddr_2:
        nop
        nop

        j fail

        target_2:
        la  x2, linkaddr_2
        bne x2, x4, fail
        ''']
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'ra', 3, '''
            li  ra, 1; \\
            jal x0, 1f; \\
            addi ra, ra, 1; \\
            addi ra, ra, 1; \\
            addi ra, ra, 1; \\
            addi ra, ra, 1; \\
        1:  addi ra, ra, 1; \\
            addi ra, ra, 1; \\
            '''
        ]
    ]
    params = { 'test_macro': param_macro, 
    'test_case': param_case }

class Test_jalr(BaseTest_jal):
    inst = Jalr
    argnames = { 'test_macro': ['macro'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_src1_bypass': ['nop_cycles']
    }
    param_macro = [
        [  
            #-------------------------------------------------------------
            # Test 2: Basic test
            #-------------------------------------------------------------
            '''
            test_2:
            li  TESTNUM, 2
            li  t0, 0
            la  t1, target_2

            jalr t0, t1, 0
            linkaddr_2:
            j fail

            target_2:
            la  t1, linkaddr_2
            bne t0, t1, fail
            '''
        ],
        [
            #-------------------------------------------------------------
            # Test 3: Basic test2, rs = rd
            #-------------------------------------------------------------
            '''
            test_3:
            li  TESTNUM, 3
            la  t0, target_3

            jalr t0, t0, 0
            linkaddr_3:
            j fail

            target_3:
            la  t1, linkaddr_3
            bne t0, t1, fail
            '''                                  
        ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 't0', 4, '''
            li  t0, 1; \\
            la  t1, 1f; \\
            jr  t1, -4; \\
            addi t0, t0, 1; \\
            addi t0, t0, 1; \\
            addi t0, t0, 1; \\
            addi t0, t0, 1; \\
        1:  addi t0, t0, 1; \\
            addi t0, t0, 1; \\
            '''
        ]
    ]
    param_src1_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------
        [ 0 ], 
        [ 1 ],
        [ 2 ],
    ]
    params = { 'test_macro': param_macro, 
    'test_case': param_case,
    'test_src1_bypass':param_src1_bypass 
    }

    def test_src1_bypass( self, nop_cycles ):
        simulate( self, Case_src1_bypass, nop_cycles=nop_cycles )

    def test_case(self, testreg, correctval, code):
        simulate( self, Case_case_jalr, testreg=testreg, correctval=correctval, code=code )

    
