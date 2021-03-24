import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvm.mul import *
from isa.rvm.mulh import *
from isa.rvm.mulhu import *
from isa.rvm.mulhsu import *
from isa.rvm.div import *
from isa.rvm.divu import *
from isa.rvm.rem import *
from isa.rvm.remu import *


class BaseCase_rvm_rr(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    footer = ''

class Case_rr_op(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_OP( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src1_eq_dest(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC1_EQ_DEST( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src2_eq_dest(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC2_EQ_DEST( {num}, {name}, {res}, {rs1}, {rs2} );'

class Case_src12_eq_dest(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_SRC12_EQ_DEST( {num}, {name}, {res}, {rs1} );'

class Case_dest_bypass(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2, nop_cycles ):
        return f'TEST_RR_DEST_BYPASS( {num}, {nop_cycles}, {name}, {res}, {rs1}, {rs2} );'

class Case_src12_bypass(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2, src1_nops, src2_nops ):
        return f'TEST_RR_SRC12_BYPASS( {num}, {src1_nops}, {src2_nops}, {name}, {res}, {rs1}, {rs2} );'

class Case_src21_bypass(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2, src1_nops, src2_nops ):
        return f'TEST_RR_SRC21_BYPASS( {num}, {src1_nops}, {src2_nops}, {name}, {res}, {rs1}, {rs2} );'

class Case_rr_zerosrc1(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC1( {num}, {name}, {res}, {rs2} );'

class Case_rr_zerosrc2(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC2( {num}, {name}, {res}, {rs1} );'

class Case_rr_zerosrc12(BaseCase_rvm_rr):
    def template(self, num, name, res, rs1, rs2 ):
        return f'TEST_RR_ZEROSRC12( {num}, {name}, {res} );'

class Case_rr_zerodest(BaseCase_rvm_rr):
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

class BaseTest_rvm_rr(BaseTest):

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
        
class Test_mul(BaseTest_rvm_rr):
    inst = Mul
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

        [ 0x00007e00, 0xb6db6db7 ],
        [ 0x00007fc0, 0xb6db6db7 ],

        [ 0x00000000, 0x00000000 ],
        [ 0x00000001, 0x00000001 ],
        [ 0x00000003, 0x00000007 ],

        [ 0x00000000, 0xffff8000 ],
        [ 0x80000000, 0x00000000 ],
        [ 0x80000000, 0xffff8000 ],

        [ 0xaaaaaaab, 0x0002fe7d ],
        [ 0x0002fe7d, 0xaaaaaaab ],

        [ 0xff000000, 0xff000000 ],

        [ 0xffffffff, 0xffffffff ],
        [ 0xffffffff, 0x00000001 ],
        [ 0x00000001, 0xffffffff ],
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
        [ 31 ],
    ]
    param_zerosrc2 = [
        [ 32 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 33, 34 ],
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

class Test_mulh(BaseTest_rvm_rr):
    inst = Mulh
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

        [ 0x00000000, 0xffff8000 ],
        [ 0x80000000, 0x00000000 ],
        [ 0x80000000, 0x00000000 ],


        [ 0xaaaaaaab, 0x0002fe7d ],
        [ 0x0002fe7d, 0xaaaaaaab ],

        [ 0xff000000, 0xff000000 ],

        [ 0xffffffff, 0xffffffff ],
        [ 0xffffffff, 0x00000001 ],
        [ 0x00000001, 0xffffffff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 13<<20, 11<<20 ],
    ]
    param_src2_eq_dest = [
        [ 14<<20, 11<<20 ],
        
    ]
    param_src12_eq_dest = [
        [ 13<<20 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13<<20, 11<<20, 0 ],
        [ 14<<20, 11<<20, 1 ],
        [ 15<<20, 11<<20, 2 ],
    ]
    param_src12_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 31<<26 ],
    ]
    param_zerosrc2 = [
        [ 32<<26 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 33<<20, 34<<20 ],
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

class Test_mulhu(BaseTest_rvm_rr):
    inst = Mulhu
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

        [ 0x00000000, 0xffff8000 ],
        [ 0x80000000, 0x00000000 ],
        [ 0x80000000, 0xffff8000 ],


        [ 0xaaaaaaab, 0x0002fe7d ],
        [ 0x0002fe7d, 0xaaaaaaab ],

        [ 0xff000000, 0xff000000 ],

        [ 0xffffffff, 0xffffffff ],
        [ 0xffffffff, 0x00000001 ],
        [ 0x00000001, 0xffffffff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 13<<20, 11<<20 ],
    ]
    param_src2_eq_dest = [
        [ 14<<20, 11<<20 ],
        
    ]
    param_src12_eq_dest = [
        [ 13<<20 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13<<20, 11<<20, 0 ],
        [ 14<<20, 11<<20, 1 ],
        [ 15<<20, 11<<20, 2 ],
    ]
    param_src12_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 31<<26 ],
    ]
    param_zerosrc2 = [
        [ 32<<26 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 33<<20, 34<<20 ],
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

class Test_mulhsu(BaseTest_rvm_rr):
    inst = Mul
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

        [ 0x00000000, 0xffff8000 ],
        [ 0x80000000, 0x00000000 ],
        [ 0x80000000, 0xffff8000 ],


        [ 0xaaaaaaab, 0x0002fe7d ],
        [ 0x0002fe7d, 0xaaaaaaab ],

        [ 0xff000000, 0xff000000 ],

        [ 0xffffffff, 0xffffffff ],
        [ 0xffffffff, 0x00000001 ],
        [ 0x00000001, 0xffffffff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 13<<20, 11<<20 ],
    ]
    param_src2_eq_dest = [
        [ 14<<20, 11<<20 ],
        
    ]
    param_src12_eq_dest = [
        [ 13<<20 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13<<20, 11<<20, 0 ],
        [ 14<<20, 11<<20, 1 ],
        [ 15<<20, 11<<20, 2 ],
    ]
    param_src12_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_src21_bypass = [
        [ 13<<20, 11<<20, 0, 0 ],
        [ 14<<20, 11<<20, 0, 1 ],
        [ 15<<20, 11<<20, 0, 2 ],
        [ 13<<20, 11<<20, 1, 0 ],
        [ 14<<20, 11<<20, 1, 1 ],
        [ 15<<20, 11<<20, 2, 0 ],
    ]
    param_zerosrc1 = [
        [ 31<<26 ],
    ]
    param_zerosrc2 = [
        [ 32<<26 ],
    ]
    param_zerosrc12 = [

    ]
    param_zerodest = [
        [ 33<<20, 34<<20 ],
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

class Only_RR_OP_Test:
    def test_src1_eq_dest(self):
        pass
    
    def test_src2_eq_dest(self):
        pass

    def test_src12_eq_dest(self):
        pass

    def test_dest_bypass(self):
        pass

    def test_src12_bypass(self):
        pass

    def test_src21_bypass(self):
        pass

    def test_zerosrc1(self):
        pass

    def test_zerosrc2(self):
        pass

    def test_zerosrc12(self):
        pass
        
    def test_zerodest(self):
        pass

class Test_div(Only_RR_OP_Test, BaseTest_rvm_rr):
    inst = Div
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
        [  20,  6 ],
        [ -20,  6 ],
        [  20, -6 ],
        [ -20, -6 ],

        [ -1<<31,  1 ],
        [ -1<<31, -1 ],

        [ -1<<31, 0 ],
        [      1, 0 ],
        [      0, 0 ],
    ]
    param_src1_eq_dest = []
    param_src2_eq_dest = []
    param_src12_eq_dest = []
    param_dest_bypass = []
    param_src12_bypass = []
    param_src21_bypass = []
    param_zerosrc1 = []
    param_zerosrc2 = []
    param_zerosrc12 = []
    param_zerodest = []
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

class Test_divu(Only_RR_OP_Test, BaseTest_rvm_rr):
    inst = Divu
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
        [  20,  6 ],
        [ -20,  6 ],
        [  20, -6 ],
        [ -20, -6 ],

        [ -1<<31,  1 ],
        [ -1<<31, -1 ],

        [ -1<<31, 0 ],
        [      1, 0 ],
        [      0, 0 ],
    ]
    param_src1_eq_dest = []
    param_src2_eq_dest = []
    param_src12_eq_dest = []
    param_dest_bypass = []
    param_src12_bypass = []
    param_src21_bypass = []
    param_zerosrc1 = []
    param_zerosrc2 = []
    param_zerosrc12 = []
    param_zerodest = []
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

class Test_rem(Only_RR_OP_Test, BaseTest_rvm_rr):
    inst = Rem
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
        [  20,  6 ],
        [ -20,  6 ],
        [  20, -6 ],
        [ -20, -6 ],

        [ -1<<31,  1 ],
        [ -1<<31, -1 ],

        [ -1<<31, 0 ],
        [      1, 0 ],
        [      0, 0 ],
    ]
    param_src1_eq_dest = []
    param_src2_eq_dest = []
    param_src12_eq_dest = []
    param_dest_bypass = []
    param_src12_bypass = []
    param_src21_bypass = []
    param_zerosrc1 = []
    param_zerosrc2 = []
    param_zerosrc12 = []
    param_zerodest = []
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

class Test_remu(Only_RR_OP_Test, BaseTest_rvm_rr):
    inst = Remu
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
        [  20,  6 ],
        [ -20,  6 ],
        [  20, -6 ],
        [ -20, -6 ],

        [ -1<<31,  1 ],
        [ -1<<31, -1 ],

        [ -1<<31, 0 ],
        [      1, 0 ],
        [      0, 0 ],
    ]
    param_src1_eq_dest = []
    param_src2_eq_dest = []
    param_src12_eq_dest = []
    param_dest_bypass = []
    param_src12_bypass = []
    param_src21_bypass = []
    param_zerosrc1 = []
    param_zerosrc2 = []
    param_zerosrc12 = []
    param_zerodest = []
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
