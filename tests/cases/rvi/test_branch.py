import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.beq import *
from isa.rvi.bne import *
from isa.rvi.blt import *
from isa.rvi.bltu import *
from isa.rvi.bge import *
from isa.rvi.bgeu import *

class BaseCase_b(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    footer = ''


class Case_br2_op_taken(BaseCase_b):
    def template( self, num, name, result, val1, val2 ):
        return f'TEST_BR2_OP_TAKEN( {num}, {name}, {val1}, {val2} )'

class Case_br2_op_nottaken(BaseCase_b):
    def template( self, num, name, result, val1, val2 ):
        return f'TEST_BR2_OP_NOTTAKEN( {num}, {name}, {val1}, {val2} )'

class Case_src12_bypass(BaseCase_b):
    def template( self, num, name, result, val1, val2, src1_nops, src2_nops ):
        return f'TEST_BR2_SRC12_BYPASS( {num}, {src1_nops}, {src2_nops}, {name}, {val1}, {val2} )'

class Case_case(BaseCase_b):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} )'



def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_b(BaseTest):

    def test_br2_op_taken(self, val1, val2):
        simulate( self, Case_br2_op_taken, val1=val1, val2=val2 )

    def test_br2_op_nottaken(self, val1, val2):
        simulate( self, Case_br2_op_nottaken, val1=val1, val2=val2 )
    def test_src12_bypass(self, val1, val2, src1_nops, src2_nops):
        simulate( self, Case_src12_bypass, val1=val1, val2=val2, src1_nops=src1_nops, src2_nops=src2_nops )

    def test_case(self, testreg, correctval, code):
        simulate( self, Case_case, testreg=testreg, correctval=correctval, code=code )

class Test_beq(BaseTest_b):
    inst = Beq
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [  0,  0 ],
        [  1,  1 ],
        [ -1, -1 ],

    ]
    param_br2_op_nottaken = [

        [  0,  1 ],
        [  1,  0 ],
        [ -1,  1 ],
        [  1, -1 ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ 0, -1, 0, 0 ],
        [ 0, -1, 0, 1 ],
        [ 0, -1, 0, 2 ],
        [ 0, -1, 1, 0 ],
        [ 0, -1, 1, 1 ],
        [ 0, -1, 2, 0 ],

        [ 0, -1, 0, 0 ],
        [ 0, -1, 0, 1 ],
        [ 0, -1, 0, 2 ],
        [ 0, -1, 1, 0 ],
        [ 0, -1, 1, 1 ],
        [ 0, -1, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            beq x0, x0, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }

class Test_bne(BaseTest_b):
    inst = Bne
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [  0,  1 ],
        [  1,  0 ],
        [ -1,  1 ],
        [  1, -1 ],

    ]
    param_br2_op_nottaken = [

        [  0,  0 ],
        [  1,  1 ],
        [ -1, -1 ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 1 ],
        [ 0, 0, 0, 2 ],
        [ 0, 0, 1, 0 ],
        [ 0, 0, 1, 1 ],
        [ 0, 0, 2, 0 ],

        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 1 ],
        [ 0, 0, 0, 2 ],
        [ 0, 0, 1, 0 ],
        [ 0, 0, 1, 1 ],
        [ 0, 0, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            bne x1, x0, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }

class Test_blt(BaseTest_b):
    inst = Blt
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [  0,  1 ],
        [ -1,  1 ],
        [ -2, -1 ],

    ]
    param_br2_op_nottaken = [

        [  1,  0 ],
        [  1, -1 ],
        [ -1, -2 ],
        [  1, -2 ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ 0, -1, 0, 0 ],
        [ 0, -1, 0, 1 ],
        [ 0, -1, 0, 2 ],
        [ 0, -1, 1, 0 ],
        [ 0, -1, 1, 1 ],
        [ 0, -1, 2, 0 ],

        [ 0, -1, 0, 0 ],
        [ 0, -1, 0, 1 ],
        [ 0, -1, 0, 2 ],
        [ 0, -1, 1, 0 ],
        [ 0, -1, 1, 1 ],
        [ 0, -1, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            blt x0, x1, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }

class Test_bltu(BaseTest_b):
    inst = Bltu
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [ 0x00000000, 0x00000001 ],
        [ 0xfffffffe, 0xffffffff ],
        [ 0x00000000, 0xffffffff ],

    ]
    param_br2_op_nottaken = [

        [ 0x00000001, 0x00000000 ],
        [ 0xffffffff, 0xfffffffe ],
        [ 0xffffffff, 0x00000000 ],
        [ 0x80000000, 0x7fffffff ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ 0xf0000000, 0xefffffff, 0, 0 ],
        [ 0xf0000000, 0xefffffff, 0, 1 ],
        [ 0xf0000000, 0xefffffff, 0, 2 ],
        [ 0xf0000000, 0xefffffff, 1, 0 ],
        [ 0xf0000000, 0xefffffff, 1, 1 ],
        [ 0xf0000000, 0xefffffff, 2, 0 ],

        [ 0xf0000000, 0xefffffff, 0, 0 ],
        [ 0xf0000000, 0xefffffff, 0, 1 ],
        [ 0xf0000000, 0xefffffff, 0, 2 ],
        [ 0xf0000000, 0xefffffff, 1, 0 ],
        [ 0xf0000000, 0xefffffff, 1, 1 ],
        [ 0xf0000000, 0xefffffff, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            bltu x0, x1, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }

class Test_bge(BaseTest_b):
    inst = Bge
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [ 0, 0 ],
        [ 1, 1 ],
        [ -1, -1 ],
        [ 1, 0 ],
        [ 1, -1 ],
        [ -1, -2],

    ]
    param_br2_op_nottaken = [

        [ 0, 1 ],
        [ -1, 1 ],
        [ -2, -1 ],
        [ -2, 1 ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ -1, 0, 0, 0 ],
        [ -1, 0, 0, 1 ],
        [ -1, 0, 0, 2 ],
        [ -1, 0, 1, 0 ],
        [ -1, 0, 1, 1 ],
        [ -1, 0, 2, 0 ],

        [ -1, 0, 0, 0 ],
        [ -1, 0, 0, 1 ],
        [ -1, 0, 0, 2 ],
        [ -1, 0, 1, 0 ],
        [ -1, 0, 1, 1 ],
        [ -1, 0, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            bge x1, x0, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }

class Test_bgeu(BaseTest_b):
    inst = Bgeu
    argnames = { 'test_br2_op_taken': ['val1', 'val2'], 
    'test_br2_op_nottaken': ['val1', 'val2'], 
    'test_src12_bypass': ['val1', 'val2', 'src1_nops', 'src2_nops'],
    'test_case': ['testreg', 'correctval', 'code'],
    }
        #-------------------------------------------------------------
        # Branch tests
        #-------------------------------------------------------------

        # Each test checks both forward and backward branches
    param_br2_op_taken = [

        [ 0x00000000, 0x00000000 ],
        [ 0x00000001, 0x00000001 ],
        [ 0xffffffff, 0xffffffff ],
        [ 0x00000001, 0x00000000 ],
        [ 0xffffffff, 0xfffffffe ],
        [ 0xffffffff, 0x00000000 ],

    ]
    param_br2_op_nottaken = [

        [ 0x00000000, 0x00000001 ],
        [ 0xfffffffe, 0xffffffff ],
        [ 0x00000000, 0xffffffff ],
        [ 0x7fffffff, 0x80000000 ],

    ]
    param_src12_bypass = [
        #-------------------------------------------------------------
        # Bypassing tests
        #-------------------------------------------------------------

        [ 0xefffffff, 0xf0000000, 0, 0 ],
        [ 0xefffffff, 0xf0000000, 0, 1 ],
        [ 0xefffffff, 0xf0000000, 0, 2 ],
        [ 0xefffffff, 0xf0000000, 1, 0 ],
        [ 0xefffffff, 0xf0000000, 1, 1 ],
        [ 0xefffffff, 0xf0000000, 2, 0 ],

        [ 0xefffffff, 0xf0000000, 0, 0 ],
        [ 0xefffffff, 0xf0000000, 0, 1 ],
        [ 0xefffffff, 0xf0000000, 0, 2 ],
        [ 0xefffffff, 0xf0000000, 1, 0 ],
        [ 0xefffffff, 0xf0000000, 1, 1 ],
        [ 0xefffffff, 0xf0000000, 2, 0 ],
    ]
    param_case = [
        #-------------------------------------------------------------
        # Test delay slot instructions not executed nor bypassed
        #-------------------------------------------------------------
        [ 'x1', 3, '''
            li  x1, 1; \\
            bgeu x1, x0, 1f; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            addi x1, x1, 1; \\
        1:  addi x1, x1, 1; \\
            addi x1, x1, 1; \\
            '''
        ],
    ]
    params = { 'test_br2_op_taken': param_br2_op_taken,
    'test_br2_op_nottaken': param_br2_op_nottaken,
    'test_src12_bypass': param_src12_bypass, 
    'test_case': param_case }