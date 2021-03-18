import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.add import *
from isa.rvi.slt import *
from isa.rvi.sltu import *
from isa.rvi.and_ import *
from isa.rvi.or_ import *
from isa.rvi.xor import *
from isa.rvi.sll import *
from isa.rvi.srl import *
from isa.rvi.sra import *
from isa.rvi.sub import *

class BaseCase_rvi_rr(BaseCase):
    head = '#include "exception.h"'
    env = 'RVTEST_RV32U'

class Case_rr_op(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_OP( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src1_eq_dest(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC1_EQ_DEST( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src2_eq_dest(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC2_EQ_DEST( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src12_eq_dest(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC12_EQ_DEST( {num}, {name}, {res}, {rs1} );'

class Case_dest_bypass(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2, nop_cycles ):
        return f'TEST_RR_DEST_BYPASS( {num}, {nop_cycles}, {name}, {res}, {rs1}, {rs2} );'

class Case_src12_bypass(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2, src1_nops, src2_nops ):
        return f'TEST_RR_SRC12_BYPASS( {num}, {src1_nops}, {src2_nops}, {name}, {res}, {rs1}, {rs2} );'

class Case_src21_bypass(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2, src1_nops, src2_nops ):
        return f'TEST_RR_SRC21_BYPASS( {num}, {src1_nops}, {src2_nops}, {name}, {res}, {rs1}, {rs2} );'

class Case_rr_zerosrc1(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC1( {num}, {name}, {res}, {rs2} );'

class Case_rr_zerosrc2(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC2( {num}, {name}, {res}, {rs1} );'

class Case_rr_zerosrc12(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC12( {num}, {name}, {res} );'

class Case_rr_zerodest(BaseCase_rvi_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZERODEST( {num}, {name}, {rs1}, {rs2} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    if len( params ):
        metafunc.parametrize(
            argnames, [ param for param in params ]
            )

class BaseTest_rvi_rr(BaseTest):

    def test_arithmetic(self, rs1, rs2):
        simulate(self, Case_rr_op, rs1=rs1, rs2=rs2)

    def test_src1_eq_dest(self, rs1, rs2):
        simulate(self, Case_src1_eq_dest, rs1=rs1, rs2=rs2)
    
    def test_src2_eq_dest(self, rs1, rs2):
        simulate(self, Case_src2_eq_dest, rs1=rs1, rs2=rs2)

    def test_src12_eq_dest(self, rs1):
        simulate(self, Case_src12_eq_dest, rs1=rs1, rs2=rs1)

    def test_dest_bypass(self, rs1, rs2, nop_cycles):
        simulate(self, Case_dest_bypass, rs1=rs1, rs2=rs2, nop_cycles=nop_cycles)

    def test_src12_bypass(self, rs1, rs2, src1_nops, src2_nops):
        simulate(self, Case_src12_bypass, rs1=rs1, rs2=rs2, src1_nops=src1_nops, src2_nops=src2_nops)

    def test_src21_bypass(self, rs1, rs2, src1_nops, src2_nops):
        simulate(self, Case_src21_bypass, rs1=rs1, rs2=rs2, src1_nops=src1_nops, src2_nops=src2_nops)

    def test_zerosrc1(self, rs2):
        simulate(self, Case_rr_zerosrc1, rs1=0, rs2=rs2)

    def test_zerosrc2(self, rs1):
        simulate(self, Case_rr_zerosrc2, rs1=rs1, rs2=0)

    def test_zerosrc12(self):
        simulate(self, Case_rr_zerosrc12, rs1=0, rs2=0)
        
    def test_zerodest(self, rs1, rs2):
        simulate(self, Case_rr_zerodest, rs1=rs1, rs2=rs2)
        
class Test_add(BaseTest_rvi_rr):
    inst = Add
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x00000000, 0x00000000 ],
        [ 0x00000001, 0x00000001 ],
        [ 0x00000003, 0x00000007 ],

        [ 0x0000000000000000, 0xffffffffffff8000 ],
        [ 0xffffffff80000000, 0x00000000 ],
        [ 0xffffffff80000000, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0x0000000000000000 ],
        [ 0x000000007fffffff, 0x0000000000007fff ],

        [ 0xffffffff80000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0xffffffffffffffff ],
        [ 0xffffffffffffffff, 0x0000000000000001 ],
        [ 0xffffffffffffffff, 0xffffffffffffffff ],

        [ 0x0000000000000001, 0x000000007fffffff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 13, 11 ],
    ]
    param_src2_eq_dest = [
        [ 14, 11 ],
        
    ]
    param_src12_eq_dest = [
        [ 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13, 11, 0 ],
        [ 14, 11, 1 ],
        [ 15, 11, 2 ],
    ]
    param_src12_bypass = [
        [ 13, 11, 0, 0 ],
        [ 14, 11, 0, 1 ],
        [ 15, 11, 0, 2 ],
        [ 13, 11, 1, 0 ],
        [ 14, 11, 1, 1 ],
        [ 15, 11, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 13, 11, 0, 0 ],
        [ 14, 11, 0, 1 ],
        [ 15, 11, 0, 2 ],
        [ 13, 11, 1, 0 ],
        [ 14, 11, 1, 1 ],
        [ 15, 11, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 15 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 16, 30 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_slt(BaseTest_rvi_rr):
    inst = Slt 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x0000000000000000, 0x0000000000000000 ],
        [ 0x0000000000000001, 0x0000000000000001 ],
        [ 0x0000000000000003, 0x0000000000000007 ],
        [ 0x0000000000000007, 0x0000000000000003 ],

        [ 0x0000000000000000, 0xffffffffffff8000 ],
        [ 0xffffffff80000000, 0x0000000000000000 ],
        [ 0xffffffff80000000, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0x0000000000000000 ],
        [ 0x000000007fffffff, 0x0000000000007fff ],

        [ 0xffffffff80000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0xffffffffffffffff ],
        [ 0xffffffffffffffff, 0x0000000000000001 ],
        [ 0xffffffffffffffff, 0xffffffffffffffff ],
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 14, 13 ],
    ]
    param_src2_eq_dest = [
        [ 11, 13 ],
    ]
    param_src12_eq_dest = [
        [ 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 11, 13, 0 ],
        [ 14, 13, 1 ],
        [ 12, 13, 2 ],
    ]
    param_src12_bypass = [
        [ 14, 13, 0, 0 ],
        [ 11, 13, 0, 1 ],
        [ 15, 13, 0, 2 ],
        [ 10, 13, 1, 0 ],
        [ 16, 13, 1, 1 ],
        [  9, 13, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 17, 13, 0, 0 ],
        [  8, 13, 0, 1 ],
        [ 18, 13, 0, 2 ],
        [  7, 13, 1, 0 ],
        [ 19, 13, 1, 1 ],
        [  6, 13, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ -1 ],
    ]
    param_zerosrc2 = [
        [ -1 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 16, 30 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }


class Test_slt(BaseTest_rvi_rr):
    inst = Slt 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x0000000000000000, 0x0000000000000000 ],
        [ 0x0000000000000001, 0x0000000000000001 ],
        [ 0x0000000000000003, 0x0000000000000007 ],
        [ 0x0000000000000007, 0x0000000000000003 ],

        [ 0x0000000000000000, 0xffffffffffff8000 ],
        [ 0xffffffff80000000, 0x0000000000000000 ],
        [ 0xffffffff80000000, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0x0000000000000000 ],
        [ 0x000000007fffffff, 0x0000000000007fff ],

        [ 0xffffffff80000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0xffffffffffffffff ],
        [ 0xffffffffffffffff, 0x0000000000000001 ],
        [ 0xffffffffffffffff, 0xffffffffffffffff ],
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 14, 13 ],
    ]
    param_src2_eq_dest = [
        [ 11, 13 ],
    ]
    param_src12_eq_dest = [
        [ 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 11, 13, 0 ],
        [ 14, 13, 1 ],
        [ 12, 13, 2 ],
    ]
    param_src12_bypass = [
        [ 14, 13, 0, 0 ],
        [ 11, 13, 0, 1 ],
        [ 15, 13, 0, 2 ],
        [ 10, 13, 1, 0 ],
        [ 16, 13, 1, 1 ],
        [  9, 13, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 17, 13, 0, 0 ],
        [  8, 13, 0, 1 ],
        [ 18, 13, 0, 2 ],
        [  7, 13, 1, 0 ],
        [ 19, 13, 1, 1 ],
        [  6, 13, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ -1 ],
    ]
    param_zerosrc2 = [
        [ -1 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 16, 30 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_sltu(BaseTest_rvi_rr):
    inst = Sltu 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x00000000, 0x00000000 ],
        [ 0x00000001, 0x00000001 ],
        [ 0x00000003, 0x00000007 ],
        [ 0x00000007, 0x00000003 ],

        [ 0x00000000, 0xffff8000 ],
        [ 0x80000000, 0x00000000 ],
        [ 0x80000000, 0xffff8000 ],

        [ 0x00000000, 0x00007fff ],
        [ 0x7fffffff, 0x00000000 ],
        [ 0x7fffffff, 0x00007fff ],

        [ 0x80000000, 0x00007fff ],
        [ 0x7fffffff, 0xffff8000 ],

        [ 0x00000000, 0xffffffff ],
        [ 0xffffffff, 0x00000001 ],
        [ 0xffffffff, 0xffffffff ],
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 14, 13 ],
    ]
    param_src2_eq_dest = [
        [ 11, 13 ],
    ]
    param_src12_eq_dest = [
        [ 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 11, 13, 0 ],
        [ 14, 13, 1 ],
        [ 12, 13, 2 ],
    ]
    param_src12_bypass = [
        [ 14, 13, 0, 0 ],
        [ 11, 13, 0, 1 ],
        [ 15, 13, 0, 2 ],
        [ 10, 13, 1, 0 ],
        [ 16, 13, 1, 1 ],
        [  9, 13, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 17, 13, 0, 0 ],
        [  8, 13, 0, 1 ],
        [ 18, 13, 0, 2 ],
        [  7, 13, 1, 0 ],
        [ 19, 13, 1, 1 ],
        [  6, 13, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ -1 ],
    ]
    param_zerosrc2 = [
        [ -1 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 16, 30 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_and(BaseTest_rvi_rr):
    inst = And 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------    

        [ 0xff00ff00, 0x0f0f0f0f ],
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
        [ 0x00ff00ff, 0x0f0f0f0f ],
        [ 0xf00ff00f, 0xf0f0f0f0 ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0xff00ff00, 0x0f0f0f0f ],
    ]
    param_src2_eq_dest = [
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
    ]
    param_src12_eq_dest = [
        [ 0xff00ff00 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2 ],
    ]
    param_src12_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 0xff00ff00 ],
    ]
    param_zerosrc2 = [
        [ 0x00ff00ff ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 0x11111111, 0x22222222 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_or(BaseTest_rvi_rr):
    inst = Or 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------    

        [ 0xff00ff00, 0x0f0f0f0f ],
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
        [ 0x00ff00ff, 0x0f0f0f0f ],
        [ 0xf00ff00f, 0xf0f0f0f0 ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0xff00ff00, 0x0f0f0f0f ],
    ]
    param_src2_eq_dest = [
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
    ]
    param_src12_eq_dest = [
        [ 0xff00ff00 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2 ],
    ]
    param_src12_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 0xff00ff00 ],
    ]
    param_zerosrc2 = [
        [ 0x00ff00ff ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 0x11111111, 0x22222222 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_xor(BaseTest_rvi_rr):
    inst = Xor 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------    

        [ 0xff00ff00, 0x0f0f0f0f ],
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
        [ 0x00ff00ff, 0x0f0f0f0f ],
        [ 0xf00ff00f, 0xf0f0f0f0 ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0xff00ff00, 0x0f0f0f0f ],
    ]
    param_src2_eq_dest = [
        [ 0x0ff00ff0, 0xf0f0f0f0 ],
    ]
    param_src12_eq_dest = [
        [ 0xff00ff00 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2 ],
    ]
    param_src12_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0xff00ff00, 0x0f0f0f0f, 0, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 0, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 0, 2 ],
        [ 0xff00ff00, 0x0f0f0f0f, 1, 0 ],
        [ 0x0ff00ff0, 0xf0f0f0f0, 1, 1 ],
        [ 0x00ff00ff, 0x0f0f0f0f, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 0xff00ff00 ],
    ]
    param_zerosrc2 = [
        [ 0x00ff00ff ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 0x11111111, 0x22222222 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_sll(BaseTest_rvi_rr):
    inst = Sll 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------   

        [ 0x0000000000000001, 0 ],
        [ 0x0000000000000001, 1 ],
        [ 0x0000000000000001, 7 ],
        [ 0x0000000000000001, 14 ],
        [ 0x0000000000000001, 31 ],

        [ 0xffffffffffffffff, 0 ],
        [ 0xffffffffffffffff, 1 ],
        [ 0xffffffffffffffff, 7 ],
        [ 0xffffffffffffffff, 14 ],
        [ 0xffffffffffffffff, 31 ],

        [ 0x0000000021212121, 0 ],
        [ 0x0000000021212121, 1 ],
        [ 0x0000000021212121, 7 ],
        [ 0x0000000021212121, 14 ],
        [ 0x0000000021212121, 31 ],

        [ 0x0000000021212121, 0xffffffffffffffc0 ],
        [ 0x0000000021212121, 0xffffffffffffffc1 ],
        [ 0x0000000021212121, 0xffffffffffffffc7 ],
        [ 0x0000000021212121, 0xffffffffffffffce ],

        #if __riscv_xlen == 64
        [ 0x0000000021212121, 0xffffffffffffffff ],
        [ 0x0000000000000001, 63 ],
        [ 0xffffffffffffffff, 39 ],
        [ 0x0000000021212121, 43 ],
        #endif
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0x00000001, 7 ],
    ]
    param_src2_eq_dest = [
        [ 0x00000001, 14 ],
    ]
    param_src12_eq_dest = [
        [ 3 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x0000000000000001, 7, 0 ],
        [ 0x0000000000000001, 14, 1 ],
        [ 0x0000000000000001, 31, 2 ],
    ]
    param_src12_bypass = [
        [ 0x0000000000000001, 7, 0, 0 ],
        [ 0x0000000000000001, 14, 0, 1 ],
        [ 0x0000000000000001, 31, 0, 2 ],
        [ 0x0000000000000001, 7, 1, 0 ],
        [ 0x0000000000000001, 14, 1, 1 ],
        [ 0x0000000000000001, 31, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0x0000000000000001, 7, 0, 0 ],
        [ 0x0000000000000001, 14, 0, 1 ],
        [ 0x0000000000000001, 31, 0, 2 ],
        [ 0x0000000000000001, 7, 1, 0 ],
        [ 0x0000000000000001, 14, 1, 1 ],
        [ 0x0000000000000001, 31, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 15 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 1024, 2048 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_srl(BaseTest_rvi_rr):
    inst = Srl 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------   

        [ 0xffffffff80000000, 0 ],
        [ 0xffffffff80000000, 1 ],
        [ 0xffffffff80000000, 7 ],
        [ 0xffffffff80000000, 14 ],
        [ 0xffffffff80000001, 31 ],

        [ 0xffffffffffffffff, 0 ],
        [ 0xffffffffffffffff, 1 ],
        [ 0xffffffffffffffff, 7 ],
        [ 0xffffffffffffffff, 14 ],
        [ 0xffffffffffffffff, 31 ],

        [ 0x0000000021212121, 0 ],
        [ 0x0000000021212121, 1 ],
        [ 0x0000000021212121, 7 ],
        [ 0x0000000021212121, 14 ],
        [ 0x0000000021212121, 31 ],

        [ 0x0000000021212121, 0xffffffffffffffc0 ],
        [ 0x0000000021212121, 0xffffffffffffffc1 ],
        [ 0x0000000021212121, 0xffffffffffffffc7 ],
        [ 0x0000000021212121, 0xffffffffffffffce ],
        [ 0x0000000021212121, 0xffffffffffffffff ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0x80000000, 7 ],
    ]
    param_src2_eq_dest = [
        [ 0x80000000, 14 ],
    ]
    param_src12_eq_dest = [
        [ 7 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x80000000, 7, 0 ],
        [ 0x80000000, 14, 1 ],
        [ 0x80000000, 31, 2 ],
    ]
    param_src12_bypass = [
        [ 0x80000000, 7, 0, 0 ],
        [ 0x80000000, 14, 0, 1 ],
        [ 0x80000000, 31, 0, 2 ],
        [ 0x80000000, 7, 1, 0 ],
        [ 0x80000000, 14, 1, 1 ],
        [ 0x80000000, 31, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0x80000000, 7, 0, 0 ],
        [ 0x80000000, 14, 0, 1 ],
        [ 0x80000000, 31, 0, 2 ],
        [ 0x80000000, 7, 1, 0 ],
        [ 0x80000000, 14, 1, 1 ],
        [ 0x80000000, 31, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 15 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 1024, 2048 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_sra(BaseTest_rvi_rr):
    inst = Sra 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------   

        [ 0xffffffff80000000, 0 ],
        [ 0xffffffff80000000, 1 ],
        [ 0xffffffff80000000, 7 ],
        [ 0xffffffff80000000, 14 ],
        [ 0xffffffff80000001, 31 ],

        [ 0x000000007fffffff, 0 ],
        [ 0x000000007fffffff, 1 ],
        [ 0x000000007fffffff, 7 ],
        [ 0x000000007fffffff, 14 ],
        [ 0x000000007fffffff, 31 ],

        [ 0xffffffff81818181, 0 ],
        [ 0xffffffff81818181, 1 ],
        [ 0xffffffff81818181, 7 ],
        [ 0xffffffff81818181, 14 ],
        [ 0xffffffff81818181, 31 ],

        [ 0xffffffff81818181, 0xffffffffffffffc0 ],
        [ 0xffffffff81818181, 0xffffffffffffffc1 ],
        [ 0xffffffff81818181, 0xffffffffffffffc7 ],
        [ 0xffffffff81818181, 0xffffffffffffffce ],
        [ 0xffffffff81818181, 0xffffffffffffffff ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 0xffffffff80000000, 7 ],
    ]
    param_src2_eq_dest = [
        [ 0xffffffff80000000, 14 ],
    ]
    param_src12_eq_dest = [
        [ 7 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xffffffff80000000, 7, 0 ],
        [ 0xffffffff80000000, 14, 1 ],
        [ 0xffffffff80000000, 31, 2 ],
    ]
    param_src12_bypass = [
        [ 0xffffffff80000000, 7, 0, 0 ],
        [ 0xffffffff80000000, 14, 0, 1 ],
        [ 0xffffffff80000000, 31, 0, 2 ],
        [ 0xffffffff80000000, 7, 1, 0 ],
        [ 0xffffffff80000000, 14, 1, 1 ],
        [ 0xffffffff80000000, 31, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 0xffffffff80000000, 7, 0, 0 ],
        [ 0xffffffff80000000, 14, 0, 1 ],
        [ 0xffffffff80000000, 31, 0, 2 ],
        [ 0xffffffff80000000, 7, 1, 0 ],
        [ 0xffffffff80000000, 14, 1, 1 ],
        [ 0xffffffff80000000, 31, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 15 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 1024, 2048 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }

class Test_sub(BaseTest_rvi_rr):
    inst = Sub 
    argnames = { 'test_arithmetic': ['rs1', 'rs2' ],
    'test_src1_eq_dest': ['rs1', 'rs2'],
    'test_src2_eq_dest': ['rs1', 'rs2'],
    'test_src12_eq_dest': ['rs1'],
    'test_dest_bypass': ['rs1', 'rs2', 'nop_cycles'],
    'test_src12_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_src21_bypass': ['rs1', 'rs2', 'src1_nops', 'src2_nops'],
    'test_zerosrc1': ['rs2'],
    'test_zerosrc2': ['rs1'],
    'test_zerosrc12': [],
    'test_zerodest': ['rs1', 'rs2']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------   

        [ 0x0000000000000000, 0x0000000000000000 ],
        [ 0x0000000000000001, 0x0000000000000001 ],
        [ 0x0000000000000003, 0x0000000000000007 ],

        [ 0x0000000000000000, 0xffffffffffff8000 ],
        [ 0xffffffff80000000, 0x0000000000000000 ],
        [ 0xffffffff80000000, 0xffffffffffff8000 ],        

        [ 0x0000000000000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0x0000000000000000 ],
        [ 0x000000007fffffff, 0x0000000000007fff ],

        [ 0xffffffff80000000, 0x0000000000007fff ],
        [ 0x000000007fffffff, 0xffffffffffff8000 ],

        [ 0x0000000000000000, 0xffffffffffffffff ],
        [ 0xffffffffffffffff, 0x0000000000000001 ],
        [ 0xffffffffffffffff, 0xffffffffffffffff ],
    
    ]
    #-------------------------------------------------------------
    # Source/Destination tests
    #-------------------------------------------------------------
    param_src1_eq_dest = [
        [ 13, 11 ],
    ]
    param_src2_eq_dest = [
        [ 14, 11 ],
    ]
    param_src12_eq_dest = [
        [ 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13, 11, 0 ],
        [ 14, 11, 1 ],
        [ 15, 11, 2 ],
    ]
    param_src12_bypass = [
        [ 13, 11, 0, 0 ],
        [ 14, 11, 0, 1 ],
        [ 15, 11, 0, 2 ],
        [ 13, 11, 1, 0 ],
        [ 14, 11, 1, 1 ],
        [ 15, 11, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 13, 11, 0, 0 ],
        [ 14, 11, 0, 1 ],
        [ 15, 11, 0, 2 ],
        [ 13, 11, 1, 0 ],
        [ 14, 11, 1, 1 ],
        [ 15, 11, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ -15 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 16, 30 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_src2_eq_dest':  param_src2_eq_dest,
    'test_src12_eq_dest':  param_src12_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerosrc2': param_zerosrc2,
    'test_zerosrc12': param_zerosrc12,
    'test_zerodest': param_zerodest }