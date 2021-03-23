import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.addi import *
from isa.rvi.slti import *
from isa.rvi.sltiu import *
from isa.rvi.andi import *
from isa.rvi.ori import *
from isa.rvi.xori import *
from isa.rvi.slli import *
from isa.rvi.srli import *
from isa.rvi.srai import *
class BaseCase_rvi_imm(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    foot = ''

class Case_imm_op(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_OP( {num}, {name}, {res}, {val1}, {imm} );'
class Case_src1_eq_dest(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_SRC1_EQ_DEST( {num}, {name}, {res}, {val1}, {imm} );'

class Case_dest_bypass(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm, nop_cycles ):
        return f'TEST_IMM_DEST_BYPASS( {num}, {nop_cycles}, {name}, {res}, {val1}, {imm} );'

class Case_src1_bypass(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm, nop_cycles ):
        return f'TEST_IMM_SRC1_BYPASS( {num}, {nop_cycles}, {name}, {res}, {val1}, {imm} );'

class Case_imm_zerosrc1(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_ZEROSRC1( {num}, {name}, {res}, {imm} );'

class Case_imm_zerodest(BaseCase_rvi_imm):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_ZERODEST( {num}, {name}, {val1}, {imm} );'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_rvi_imm(BaseTest):

    def test_arithmetic(self, rs1, imm):
        simulate(self, Case_imm_op, rs1=rs1, imm=imm)

    def test_src1_eq_dest(self, rs1, imm):
        simulate(self, Case_src1_eq_dest, rs1=rs1, imm=imm)

    def test_dest_bypass(self, rs1, imm, nop_cycles):
        simulate(self, Case_dest_bypass, rs1=rs1, imm=imm, nop_cycles=nop_cycles)

    def test_src1_bypass(self, rs1, imm, nop_cycles):
        simulate(self, Case_src1_bypass, rs1=rs1, imm=imm, nop_cycles=nop_cycles)

    def test_zerosrc1(self, imm):
        simulate(self, Case_imm_zerosrc1, rs1=0, imm=imm)
        
    def test_zerodest(self, rs1, imm):
        simulate(self, Case_imm_zerodest, rs1=rs1, imm=imm)
        
class Test_addi(BaseTest_rvi_imm):
    inst = Addi
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x00000000, 0x000 ],
        [ 0x00000001, 0x001 ],
        [ 0x00000003, 0x007 ],

        [ 0x0000000000000000, 0x800 ],
        [ 0xffffffff80000000, 0x000 ],
        [ 0xffffffff80000000, 0x800 ],

        [ 0x00000000, 0x7ff ],
        [ 0x7fffffff, 0x000 ],
        [ 0x7fffffff, 0x7ff ],

        [ 0xffffffff80000000, 0x7ff ],
        [ 0x000000007fffffff, 0x800 ],

        [ 0x0000000000000000, 0xfff ],
        [ 0xffffffffffffffff, 0x001 ],
        [ 0xffffffffffffffff, 0xfff ],

        [ 0x7fffffff, 0x001 ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 13, 11 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 13, 11, 0 ],
        [ 13, 10, 1 ],
        [ 13,  9, 2 ],
    ]
    param_src1_bypass = [
        [ 13, 11, 0 ],
        [ 13, 10, 1 ],
        [ 13,  9, 2 ],
    ]
    param_zerosrc1 = [
        [ 32 ],
    ]
    param_zerodest = [
        [ 33, 50 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest }

class Test_slti(BaseTest_rvi_imm):
    inst = Slti
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ 0x0000000000000000, 0x000 ],
        [ 0x0000000000000001, 0x001 ],
        [ 0x0000000000000003, 0x007 ],
        [ 0x0000000000000007, 0x003 ],

        [ 0x0000000000000000, 0x800 ],
        [ 0xffffffff80000000, 0x000 ],
        [ 0xffffffff80000000, 0x800 ],

        [ 0x0000000000000000, 0x7ff ],
        [ 0x000000007fffffff, 0x000 ],
        [ 0x000000007fffffff, 0x7ff ],

        [ 0xffffffff80000000, 0x7ff ],
        [ 0x000000007fffffff, 0x800 ],

        [ 0x0000000000000000, 0xfff ],
        [ 0xffffffffffffffff, 0x001 ],
        [ 0xffffffffffffffff, 0xfff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 11, 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 15, 10, 0 ],
        [ 10, 16, 1 ],
        [ 16,  9, 2 ],
    ]
    param_src1_bypass = [
        [ 11, 15, 0 ],
        [ 17,  8, 1 ],
        [ 12, 14, 2 ],
    ]
    param_zerosrc1 = [
        [ 0xfff ],
    ]
    param_zerodest = [
        [ 0x00ff00ff, 0xfff ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest }

class Test_sltiu(BaseTest_rvi_imm):
    inst = Sltiu
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------
        [ 0x0000000000000000, 0x000 ],
        [ 0x0000000000000001, 0x001 ],
        [ 0x0000000000000003, 0x007 ],
        [ 0x0000000000000007, 0x003 ],

        [ 0x0000000000000000, 0x800 ],
        [ 0xffffffff80000000, 0x000 ],
        [ 0xffffffff80000000, 0x800 ],

        [ 0x0000000000000000, 0x7ff ],
        [ 0x000000007fffffff, 0x000 ],
        [ 0x000000007fffffff, 0x7ff ],

        [ 0xffffffff80000000, 0x7ff ],
        [ 0x000000007fffffff, 0x800 ],

        [ 0x0000000000000000, 0xfff ],
        [ 0xffffffffffffffff, 0x001 ],
        [ 0xffffffffffffffff, 0xfff ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 11, 13 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 15, 10, 0 ],
        [ 10, 16, 1 ],
        [ 16,  9, 2 ],
    ]
    param_src1_bypass = [
        [ 11, 15, 0 ],
        [ 17,  8, 1 ],
        [ 12, 14, 2 ],
    ]
    param_zerosrc1 = [
        [ 0xfff ],
    ]
    param_zerodest = [
        [ 0x00ff00ff, 0xfff ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest }
class Test_andi(BaseTest_rvi_imm):
    inst = Andi
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------
        [ 0xff00ff00, 0xf0f ],
        [ 0x0ff00ff0, 0x0f0 ],
        [ 0x00ff00ff, 0x70f ],
        [ 0xf00ff00f, 0x0f0 ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0xff00ff00, 0x0f0 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x0ff00ff0, 0x70f, 0 ],
        [ 0x00ff00ff, 0x0f0, 1 ],
        [ 0xf00ff00f, 0xf0f, 2 ],
    ]
    param_src1_bypass = [
        [ 0x0ff00ff0, 0x70f, 0 ],
        [ 0x00ff00ff, 0x0f0, 1 ],
        [ 0xf00ff00f, 0x70f, 2 ], 
    ]
    param_zerosrc1 = [
        [ 0X0f0 ],
    ]
    param_zerodest = [
        [ 0x00ff00ff, 0x70f ]
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest }


class Test_ori(BaseTest_rvi_imm):
    inst = Ori
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------
        [ 0xffffffffff00ff00, 0xf0f ],
        [ 0x000000000ff00ff0, 0x0f0 ],
        [ 0x0000000000ff00ff, 0x70f ],
        [ 0xfffffffff00ff00f, 0x0f0 ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0xff00ff00, 0x0f0 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x000000000ff00ff0, 0x0f0, 0 ],
        [ 0x0000000000ff00ff, 0x70f, 1 ],
        [ 0xfffffffff00ff00f, 0x0f0, 2 ],
    ]
    param_src1_bypass = [
        [ 0x000000000ff00ff0, 0x0f0, 0 ],
        [ 0x0000000000ff00ff, 0xf0f, 1 ],
        [ 0xfffffffff00ff00f, 0x0f0, 2 ],
    ]
    param_zerosrc1 = [
        [ 0x0f0 ],
    ]
    param_zerodest = [
        [ 0x00ff00ff, 0x70f ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest }  

class Test_xori(BaseTest_rvi_imm):
    inst = Xori
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Logical tests
        #-------------------------------------------------------------
        [ 0x0000000000ff0f00, 0xf0f ],
        [ 0x000000000ff00ff0, 0x0f0 ],
        [ 0x0000000000ff08ff, 0x70f ],
        [ 0xfffffffff00ff00f, 0x0f0 ],
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0xffffffffff00f700, 0x70f ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x000000000ff00ff0, 0x0f0, 0 ],
        [ 0x0000000000ff08ff, 0x70f, 1 ],
        [ 0xfffffffff00ff00f, 0x0f0, 2 ],
    ]
    param_src1_bypass = [
        [ 0x000000000ff00ff0, 0x0f0, 0 ],
        [ 0x0000000000ff0fff, 0x00f, 1 ],
        [ 0xfffffffff00ff00f, 0x0f0, 2 ],
    ]
    param_zerosrc1 = [
        [ 0x0f0 ],
    ]
    param_zerodest = [
        [ 0x00ff00ff, 0x70f ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest } 

class Test_slli(BaseTest_rvi_imm):
    inst = Slli
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0x0000000000000001, 0  ],
        [ 0x0000000000000001, 1  ],
        [ 0x0000000000000001, 7  ],
        [ 0x0000000000000001, 14 ],
        [ 0x0000000000000001, 31 ],

        [ 0xffffffffffffffff, 0  ],
        [ 0xffffffffffffffff, 1  ],
        [ 0xffffffffffffffff, 7  ],
        [ 0xffffffffffffffff, 14 ],
        [ 0xffffffffffffffff, 31 ],

        [ 0x0000000021212121, 0  ],
        [ 0x0000000021212121, 1  ],
        [ 0x0000000021212121, 7  ],
        [ 0x0000000021212121, 14 ],
        [ 0x0000000021212121, 31 ],

        #if __riscv_xlen == 64
        #[ 0x0000000000000001, 63 ],
        #[ 0xffffffffffffffff, 39 ],
        #[ 0x0000000021212121, 43 ],
        #endif
    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0x00000001, 7 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x0000000000000001, 7 , 0 ],
        [ 0x0000000000000001, 14, 1 ],
        [ 0x0000000000000001, 31, 2 ],
    ]
    param_src1_bypass = [
        [ 0x0000000000000001, 7 , 0 ],
        [ 0x0000000000000001, 14, 1 ],
        [ 0x0000000000000001, 31, 2 ],
    ]
    param_zerosrc1 = [
        [ 31 ],
    ]
    param_zerodest = [
        [ 33, 20 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest } 


class Test_srli(BaseTest_rvi_imm):
    inst = Srli
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0xffffffff80000000, 0  ],
        [ 0xffffffff80000000, 1  ],
        [ 0xffffffff80000000, 7  ],
        [ 0xffffffff80000000, 14 ],
        [ 0xffffffff80000001, 31 ],

        [ 0xffffffffffffffff, 0  ],
        [ 0xffffffffffffffff, 1  ],
        [ 0xffffffffffffffff, 7  ],
        [ 0xffffffffffffffff, 14 ],
        [ 0xffffffffffffffff, 31 ],

        [ 0x0000000021212121, 0  ],
        [ 0x0000000021212121, 1  ],
        [ 0x0000000021212121, 7  ],
        [ 0x0000000021212121, 14 ],
        [ 0x0000000021212121, 31 ],

    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0x80000000, 7 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x80000000, 7 , 0 ],
        [ 0x80000000, 14, 1 ],
        [ 0x80000001, 31, 2 ],
    ]
    param_src1_bypass = [
        [ 0x80000000, 7 , 0 ],
        [ 0x80000000, 14, 1 ],
        [ 0x80000001, 31, 2 ],
    ]
    param_zerosrc1 = [
        [ 4 ],
    ]
    param_zerodest = [
        [ 33, 10 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest } 

class Test_srai(BaseTest_rvi_imm):
    inst = Srai
    argnames = { 'test_arithmetic': ['rs1', 'imm' ],
    'test_src1_eq_dest': ['rs1', 'imm'],
    'test_dest_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_src1_bypass': ['rs1', 'imm', 'nop_cycles'],
    'test_zerosrc1': ['imm'],
    'test_zerodest': ['rs1', 'imm']}
    param_arithmetic = [
        #-------------------------------------------------------------
        # Arithmetic tests
        #-------------------------------------------------------------

        [ 0xffffff8000000000, 0  ],
        [ 0xffffffff80000000, 1  ],
        [ 0xffffffff80000000, 7  ],
        [ 0xffffffff80000000, 14 ],
        [ 0xffffffff80000001, 31 ],

        [ 0x000000007fffffff, 0  ],
        [ 0x000000007fffffff, 1  ],
        [ 0x000000007fffffff, 7  ],
        [ 0x000000007fffffff, 14 ],
        [ 0x000000007fffffff, 31 ],

        [ 0xffffffff81818181, 0  ],
        [ 0xffffffff81818181, 1  ],
        [ 0xffffffff81818181, 7  ],
        [ 0xffffffff81818181, 14 ],
        [ 0xffffffff81818181, 31 ],

    ]
    param_src1_eq_dest = [
        #-------------------------------------------------------------
        # Source/Destination tests
        #-------------------------------------------------------------

        [ 0xffffffff80000000, 7 ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xffffffff80000000, 7 , 0 ],
        [ 0xffffffff80000000, 14, 1 ],
        [ 0xffffffff80000001, 31, 2 ],
    ]
    param_src1_bypass = [
        [ 0xffffffff80000000, 7 , 0 ],
        [ 0xffffffff80000000, 14, 1 ],
        [ 0xffffffff80000001, 31, 2 ],
    ]
    param_zerosrc1 = [
        [ 4 ],
    ]
    param_zerodest = [
        [ 33, 10 ],
    ]
    params = { 'test_arithmetic': param_arithmetic,
    'test_src1_eq_dest':  param_src1_eq_dest,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass,
    'test_zerosrc1': param_zerosrc1,
    'test_zerodest': param_zerodest } 