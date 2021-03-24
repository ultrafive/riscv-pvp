import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.sb import *
from isa.rvi.sh import *
from isa.rvi.sw import *

class BaseCase_store(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    footer = ''

class Case_st_op(BaseCase_store):
    def template( self, num, name, rd, result, offset, base, load_inst ):
        return f'TEST_ST_OP({num}, {load_inst}, {name}, {result}, {offset}, {base})'
class Case_case(BaseCase_store):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} )'


class Case_src12_bypass(BaseCase_store):
    def template( self, num, name, rd, result, offset, base, src1_nops, src2_nops, load_inst ):
        return f'TEST_ST_SRC12_BYPASS( {num}, {src1_nops}, {src2_nops}, {load_inst}, {name}, {result}, {offset}, {base} )'

class Case_src21_bypass(BaseCase_store):
    def template( self, num, name, rd, result, offset, base, src1_nops, src2_nops, load_inst ):
        return f'TEST_ST_SRC21_BYPASS( {num}, {src1_nops}, {src2_nops}, {load_inst}, {name}, {result}, {offset}, {base} )'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_store(BaseTest):

    def test_st_op(self, result, offset, base, load_inst):
        simulate( self, self.Case_st_op_inst, result=result, offset=offset, base=base, load_inst=load_inst )

    def test_case(self, testreg, correctval, code):
        simulate( self, self.Case_case_inst, testreg=testreg, correctval=correctval, code=code )

    def test_src12_bypass(self, result, offset, base, src1_nops, src2_nops, load_inst):
        simulate( self, self.Case_src12_bypass_inst, result=result, offset=offset, base=base, src1_nops=src1_nops, src2_nops=src2_nops, load_inst=load_inst )

    def test_src21_bypass(self, result, offset, base, src1_nops, src2_nops, load_inst):
        simulate( self, self.Case_src21_bypass_inst, result=result, offset=offset, base=base, src1_nops=src1_nops, src2_nops=src2_nops, load_inst=load_inst )

class Test_Sb(BaseTest_store):
    inst = Sb
    argnames = { 'test_st_op': ['result', 'offset', 'base', 'load_inst'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_src12_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'], 
    'test_src21_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'],   
    }
    param_st_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------
        [ 0xffffffffffffffaa, 0, 'tdat', 'lb'  ],
        [ 0x0000000000000000, 1, 'tdat', 'lb'  ],
        [ 0xffffffffffffefa0, 2, 'tdat', 'lh'  ],
        [ 0x000000000000000a, 3, 'tdat', 'lb'  ],
        
        # Test with negative offset
        [ 0xffffffffffffffaa, -3, 'tdat8', 'lb'  ],
        [ 0x0000000000000000, -2, 'tdat8', 'lb'  ],
        [ 0xffffffffffffffa0, -1, 'tdat8', 'lb'  ],
        [ 0x000000000000000a,  0, 'tdat8', 'lb'  ],        

    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x78, '''
            la  x1, tdat9; \\
            li  x2, 0x12345678; \\
            addi x4, x1, -32; \\
            sb x2, 32(x4); \\
            lb x5, 0(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0xffffffffffffff98, '''
            la  x1, tdat9; \\
            li  x2, 0x00003098; \\
            addi x1, x1, -6; \\
            sb x2, 7(x1); \\
            la  x4, tdat10; \\
            lb x5, 0(x4); \\
            '''
        ]

    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_src12_bypass = [
        [ 0xffffffffffffffdd, 0, 'tdat', 0, 0, 'lb' ],
        [ 0xffffffffffffffcd, 1, 'tdat', 0, 1, 'lb' ],
        [ 0xffffffffffffffcc, 2, 'tdat', 0, 2, 'lb' ],
        [ 0xffffffffffffffbc, 3, 'tdat', 1, 0, 'lb' ],
        [ 0xffffffffffffffbb, 4, 'tdat', 1, 1, 'lb' ],
        [ 0xffffffffffffffab, 5, 'tdat', 2, 0, 'lb' ],

    ]
    param_src21_bypass = [
        [ 0x33, 0, 'tdat', 0, 0, 'lb' ],
        [ 0x23, 1, 'tdat', 0, 1, 'lb' ],
        [ 0x22, 2, 'tdat', 0, 2, 'lb' ],
        [ 0x12, 3, 'tdat', 1, 0, 'lb' ],
        [ 0x11, 4, 'tdat', 1, 1, 'lb' ],
        [ 0x01, 5, 'tdat', 2, 0, 'lb' ],      
    ]
    params = { 'test_st_op': param_st_op, 
    'test_case': param_case,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .byte 0xef
tdat2:  .byte 0xef
tdat3:  .byte 0xef
tdat4:  .byte 0xef
tdat5:  .byte 0xef
tdat6:  .byte 0xef
tdat7:  .byte 0xef
tdat8:  .byte 0xef
tdat9:  .byte 0xef
tdat10: .byte 0xef 
'''

    class Case_st_op_inst(Tdata, Case_st_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_src12_bypass_inst(Tdata, Case_src12_bypass ):
        pass
    class Case_src21_bypass_inst(Tdata, Case_src21_bypass ):
        pass

class Test_Sh(BaseTest_store):
    inst = Sh
    argnames = { 'test_st_op': ['result', 'offset', 'base', 'load_inst'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_src12_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'], 
    'test_src21_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'],   
    }
    param_st_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------
        [ 0x00000000000000aa, 0, 'tdat', 'lh'  ],
        [ 0xffffffffffffaa00, 2, 'tdat', 'lh'  ],
        [ 0xffffffffbeef0aa0, 4, 'tdat', 'lw'  ],
        [ 0xffffffffffffa00a, 6, 'tdat', 'lh'  ],
        
        # Test with negative offset
        [ 0x00000000000000aa, -6, 'tdat8', 'lh'  ],
        [ 0xffffffffffffaa00, -4, 'tdat8', 'lh'  ],
        [ 0x0000000000000aa0, -2, 'tdat8', 'lh'  ],
        [ 0xffffffffffffa00a,  0, 'tdat8', 'lh'  ],        

    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x5678, '''
            la  x1, tdat9; \\
            li  x2, 0x12345678; \\
            addi x4, x1, -32; \\
            sh x2, 32(x4); \\
            lh x5, 0(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0x3098, '''
            la  x1, tdat9; \\
            li  x2, 0x00003098; \\
            addi x1, x1, -5; \\
            sh x2, 7(x1); \\
            la  x4, tdat10; \\
            lh x5, 0(x4); \\
            '''
        ]

    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_src12_bypass = [
        [ 0xffffffffffffccdd, 0, 'tdat', 0, 0, 'lh' ],
        [ 0xffffffffffffbccd, 2, 'tdat', 0, 1, 'lh' ],
        [ 0xffffffffffffbbcc, 4, 'tdat', 0, 2, 'lh' ],
        [ 0xffffffffffffabbc, 6, 'tdat', 1, 0, 'lh' ],
        [ 0xffffffffffffaabb, 8, 'tdat', 1, 1, 'lh' ],
        [ 0xffffffffffffdaab, 10, 'tdat', 2, 0, 'lh' ],

    ]
    param_src21_bypass = [
        [ 0x2233, 0, 'tdat', 0, 0, 'lh' ],
        [ 0x1223, 2, 'tdat', 0, 1, 'lh' ],
        [ 0x1122, 4, 'tdat', 0, 2, 'lh' ],
        [ 0x0112, 6, 'tdat', 1, 0, 'lh' ],
        [ 0x0011, 8, 'tdat', 1, 1, 'lh' ],
        [ 0x3001, 10, 'tdat', 2, 0, 'lh' ],      
    ]
    params = { 'test_st_op': param_st_op, 
    'test_case': param_case,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .half 0xbeef
tdat2:  .half 0xbeef
tdat3:  .half 0xbeef
tdat4:  .half 0xbeef
tdat5:  .half 0xbeef
tdat6:  .half 0xbeef
tdat7:  .half 0xbeef
tdat8:  .half 0xbeef
tdat9:  .half 0xbeef
tdat10: .half 0xbeef
'''

    class Case_st_op_inst(Tdata, Case_st_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_src12_bypass_inst(Tdata, Case_src12_bypass ):
        pass
    class Case_src21_bypass_inst(Tdata, Case_src21_bypass ):
        pass

class Test_Sw(BaseTest_store):
    inst = Sw
    argnames = { 'test_st_op': ['result', 'offset', 'base', 'load_inst'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_src12_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'], 
    'test_src21_bypass': ['result', 'offset', 'base', 'src1_nops', 'src2_nops', 'load_inst'],   
    }
    param_st_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------
        [ 0x0000000000aa00aa, 0, 'tdat', 'lw'  ],
        [ 0xffffffffaa00aa00, 4, 'tdat', 'lw'  ],
        [ 0x000000000aa00aa0, 8, 'tdat', 'lw'  ],
        [ 0xffffffffa00aa00a, 12, 'tdat', 'lw'  ],
        
        # Test with negative offset
        [ 0x0000000000aa00aa, -12, 'tdat8', 'lw'  ],
        [ 0xffffffffaa00aa00, -8, 'tdat8', 'lw'  ],
        [ 0x000000000aa00aa0, -4, 'tdat8', 'lw'  ],
        [ 0xffffffffa00aa00a,  0, 'tdat8', 'lw'  ],        

    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x12345678, '''
            la  x1, tdat9; \\
            li  x2, 0x12345678; \\
            addi x4, x1, -32; \\
            sw x2, 32(x4); \\
            lw x5, 0(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0x58213098, '''
            la  x1, tdat9; \\
            li  x2, 0x58213098; \\
            addi x1, x1, -3; \\
            sw x2, 7(x1); \\
            la  x4, tdat10; \\
            lw x5, 0(x4); \\
            '''
        ]

    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_src12_bypass = [
        [ 0xffffffffaabbccdd, 0, 'tdat', 0, 0, 'lw' ],
        [ 0xffffffffdaabbccd, 4, 'tdat', 0, 1, 'lw' ],
        [ 0xffffffffddaabbcc, 8, 'tdat', 0, 2, 'lw' ],
        [ 0xffffffffcddaabbc, 12, 'tdat', 1, 0, 'lw' ],
        [ 0xffffffffccddaabb, 16, 'tdat', 1, 1, 'lw' ],
        [ 0xffffffffbccddaab, 20, 'tdat', 2, 0, 'lw' ],

    ]
    param_src21_bypass = [
        [ 0x00112233, 0, 'tdat', 0, 0, 'lw' ],
        [ 0x30011223, 4, 'tdat', 0, 1, 'lw' ],
        [ 0x33001122, 8, 'tdat', 0, 2, 'lw' ],
        [ 0x23300112, 12, 'tdat', 1, 0, 'lw' ],
        [ 0x22330011, 16, 'tdat', 1, 1, 'lw' ],
        [ 0x12233001, 20, 'tdat', 2, 0, 'lw' ],      
    ]
    params = { 'test_st_op': param_st_op, 
    'test_case': param_case,
    'test_src12_bypass': param_src12_bypass,
    'test_src21_bypass': param_src21_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .word 0xdeadbeef
tdat2:  .word 0xdeadbeef
tdat3:  .word 0xdeadbeef
tdat4:  .word 0xdeadbeef
tdat5:  .word 0xdeadbeef
tdat6:  .word 0xdeadbeef
tdat7:  .word 0xdeadbeef
tdat8:  .word 0xdeadbeef
tdat9:  .word 0xdeadbeef
tdat10: .word 0xdeadbeef
'''

    class Case_st_op_inst(Tdata, Case_st_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_src12_bypass_inst(Tdata, Case_src12_bypass ):
        pass
    class Case_src21_bypass_inst(Tdata, Case_src21_bypass ):
        pass