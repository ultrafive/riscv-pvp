import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.lb import *
from isa.rvi.lbu import *
from isa.rvi.lh import *
from isa.rvi.lhu import *
from isa.rvi.lw import *

class BaseCase_load(BaseCase):
    header = '#include "exception.h"'
    env = 'RVTEST_RV32U'
    tdata = ''
    footer = ''

class Case_ld_op(BaseCase_load):
    def template( self, num, name, rd, result, offset, base ):
        return f'TEST_LD_OP({num}, {name}, {result}, {offset}, {base})'
class Case_case(BaseCase_load):
    def template( self, num, name, rd, testreg, correctval, code ):
        return f'TEST_CASE( {num}, {testreg}, {correctval}, {code} )'

class Case_dest_bypass(BaseCase_load):
    def template( self, num, name, rd, result, offset, base, nop_cycles ):
        return f'TEST_LD_DEST_BYPASS( {num}, {nop_cycles}, {name}, {result}, {offset}, {base} )'

class Case_src1_bypass(BaseCase_load):
    def template( self, num, name, rd, result, offset, base, nop_cycles ):
        return f'TEST_LD_SRC1_BYPASS( {num}, {nop_cycles}, {name}, {result}, {offset}, {base} )'

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ param for param in params ]
    )

class BaseTest_load(BaseTest):

    def test_ld_op(self, result, offset, base):
        simulate( self, self.Case_ld_op_inst, result=result, offset=offset, base=base )

    def test_case(self, testreg, correctval, code):
        simulate( self, self.Case_case_inst, testreg=testreg, correctval=correctval, code=code )

    def test_dest_bypass(self, result, offset, base, nop_cycles):
        simulate( self, self.Case_dest_bypass_inst, result=result, offset=offset, base=base, nop_cycles=nop_cycles )

    def test_src1_bypass(self, result, offset, base, nop_cycles):
        simulate( self, self.Case_src1_bypass_inst, result=result, offset=offset, base=base, nop_cycles=nop_cycles )

class Test_lb(BaseTest_load):
    inst = Lb
    argnames = { 'test_ld_op': ['result', 'offset', 'base'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_dest_bypass': ['result', 'offset', 'base', 'nop_cycles'],
    'test_src1_bypass': ['result', 'offset', 'base', 'nop_cycles'],    
    }
    param_ld_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------

        [ 0xffffffffffffffff, 0,  'tdat' ],
        [ 0x0000000000000000, 1,  'tdat' ],
        [ 0xfffffffffffffff0, 2,  'tdat' ],
        [ 0x000000000000000f, 3,  'tdat' ],

        # Test with negative offset

        [ 0xffffffffffffffff, -3, 'tdat4' ],
        [ 0x0000000000000000, -2, 'tdat4' ],
        [ 0xfffffffffffffff0, -1, 'tdat4' ],
        [ 0x000000000000000f,  0, 'tdat4' ],        
    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0xffffffffffffffff, '''
            la  x1, tdat; \\
            addi x1, x1, -32; \\
            lb x5, 32(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0x0000000000000000, '''
            la  x1, tdat; \\
            addi x1, x1, -6; \\
            lb x5, 7(x1); \\
            '''
        ],

        #-------------------------------------------------------------
        # Test write-after-write hazard
        #-------------------------------------------------------------

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lb  x2, 0(x5); \\
            li  x2, 2; \\
            '''
        ],

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lb  x2, 0(x5); \\
            nop; \\
            li  x2, 2; \\
            '''
        ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0xfffffffffffffff0, 1, 'tdat2', 0 ],
        [ 0x000000000000000f, 1, 'tdat3', 1 ],
        [ 0x0000000000000000, 1, 'tdat1', 2 ],
    ]
    param_src1_bypass = [
        [ 0xfffffffffffffff0, 1, 'tdat2', 0 ],
        [ 0x000000000000000f, 1, 'tdat3', 1 ],
        [ 0x0000000000000000, 1, 'tdat1', 2 ],        
    ]
    params = { 'test_ld_op': param_ld_op, 
    'test_case': param_case,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .byte 0xff
tdat2:  .byte 0x00
tdat3:  .byte 0xf0
tdat4:  .byte 0x0f 
'''

    class Case_ld_op_inst(Tdata, Case_ld_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_dest_bypass_inst(Tdata, Case_dest_bypass ):
        pass
    class Case_src1_bypass_inst(Tdata, Case_src1_bypass ):
        pass
    
class Test_lbu(BaseTest_load):
    inst = Lbu
    argnames = { 'test_ld_op': ['result', 'offset', 'base'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_dest_bypass': ['result', 'offset', 'base', 'nop_cycles'],
    'test_src1_bypass': ['result', 'offset', 'base', 'nop_cycles'],    
    }
    param_ld_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------

        [ 0x00000000000000ff, 0,  'tdat' ],
        [ 0x0000000000000000, 1,  'tdat' ],
        [ 0x00000000000000f0, 2,  'tdat' ],
        [ 0x000000000000000f, 3,  'tdat' ],

        # Test with negative offset

        [ 0x00000000000000ff, -3, 'tdat4' ],
        [ 0x0000000000000000, -2, 'tdat4' ],
        [ 0x00000000000000f0, -1, 'tdat4' ],
        [ 0x000000000000000f,  0, 'tdat4' ],        
    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x00000000000000ff, '''
            la  x1, tdat; \\
            addi x1, x1, -32; \\
            lbu x5, 32(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0x0000000000000000, '''
            la  x1, tdat; \\
            addi x1, x1, -6; \\
            lbu x5, 7(x1); \\
            '''
        ],

        #-------------------------------------------------------------
        # Test write-after-write hazard
        #-------------------------------------------------------------

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lbu  x2, 0(x5); \\
            li  x2, 2; \\
            '''
        ],

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lbu  x2, 0(x5); \\
            nop; \\
            li  x2, 2; \\
            '''
        ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x00000000000000f0, 1, 'tdat2', 0 ],
        [ 0x000000000000000f, 1, 'tdat3', 1 ],
        [ 0x0000000000000000, 1, 'tdat1', 2 ],
    ]
    param_src1_bypass = [
        [ 0x00000000000000f0, 1, 'tdat2', 0 ],
        [ 0x000000000000000f, 1, 'tdat3', 1 ],
        [ 0x0000000000000000, 1, 'tdat1', 2 ],        
    ]
    params = { 'test_ld_op': param_ld_op, 
    'test_case': param_case,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .byte 0xff
tdat2:  .byte 0x00
tdat3:  .byte 0xf0
tdat4:  .byte 0x0f 
'''

    class Case_ld_op_inst(Tdata, Case_ld_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_dest_bypass_inst(Tdata, Case_dest_bypass ):
        pass
    class Case_src1_bypass_inst(Tdata, Case_src1_bypass ):
        pass

class Test_lh(BaseTest_load):
    inst = Lh
    argnames = { 'test_ld_op': ['result', 'offset', 'base'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_dest_bypass': ['result', 'offset', 'base', 'nop_cycles'],
    'test_src1_bypass': ['result', 'offset', 'base', 'nop_cycles'],    
    }
    param_ld_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------

        [ 0x00000000000000ff, 0,  'tdat' ],
        [ 0xffffffffffffff00, 2,  'tdat' ],
        [ 0x0000000000000ff0, 4,  'tdat' ],
        [ 0xfffffffffffff00f, 6,  'tdat' ],

        # Test with negative offset

        [ 0x00000000000000ff, -6,  'tdat4' ],
        [ 0xffffffffffffff00, -4,  'tdat4' ],
        [ 0x0000000000000ff0, -2,  'tdat4' ],
        [ 0xfffffffffffff00f,  0,  'tdat4' ],       
    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x00000000000000ff, '''
            la  x1, tdat; \\
            addi x1, x1, -32; \\
            lh x5, 32(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0xffffffffffffff00, '''
            la  x1, tdat; \\
            addi x1, x1, -5; \\
            lh x5, 7(x1); \\
            '''
        ],

        #-------------------------------------------------------------
        # Test write-after-write hazard
        #-------------------------------------------------------------

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lh  x2, 0(x5); \\
            li  x2, 2; \\
            '''
        ],

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lh  x2, 0(x5); \\
            nop; \\
            li  x2, 2; \\
            '''
        ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x0000000000000ff0, 2, 'tdat2', 0 ],
        [ 0xfffffffffffff00f, 2, 'tdat3', 1 ],
        [ 0xffffffffffffff00, 2, 'tdat1', 2 ],
    ]
    param_src1_bypass = [
        [ 0x0000000000000ff0, 2, 'tdat2', 0 ],
        [ 0xfffffffffffff00f, 2, 'tdat3', 1 ],
        [ 0xffffffffffffff00, 2, 'tdat1', 2 ],        
    ]
    params = { 'test_ld_op': param_ld_op, 
    'test_case': param_case,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .half 0x00ff
tdat2:  .half 0xff00
tdat3:  .half 0x0ff0
tdat4:  .half 0xf00f
'''

    class Case_ld_op_inst(Tdata, Case_ld_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_dest_bypass_inst(Tdata, Case_dest_bypass ):
        pass
    class Case_src1_bypass_inst(Tdata, Case_src1_bypass ):
        pass

class Test_lhu(BaseTest_load):
    inst = Lhu
    argnames = { 'test_ld_op': ['result', 'offset', 'base'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_dest_bypass': ['result', 'offset', 'base', 'nop_cycles'],
    'test_src1_bypass': ['result', 'offset', 'base', 'nop_cycles'],    
    }
    param_ld_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------

        [ 0x00000000000000ff, 0,  'tdat' ],
        [ 0x000000000000ff00, 2,  'tdat' ],
        [ 0x0000000000000ff0, 4,  'tdat' ],
        [ 0x000000000000f00f, 6,  'tdat' ],

        # Test with negative offset

        [ 0x00000000000000ff, -6,  'tdat4' ],
        [ 0x000000000000ff00, -4,  'tdat4' ],
        [ 0x0000000000000ff0, -2,  'tdat4' ],
        [ 0x000000000000f00f,  0,  'tdat4' ],       
    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x00000000000000ff, '''
            la  x1, tdat; \\
            addi x1, x1, -32; \\
            lhu x5, 32(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0x000000000000ff00, '''
            la  x1, tdat; \\
            addi x1, x1, -5; \\
            lhu x5, 7(x1); \\
            '''
        ],

        #-------------------------------------------------------------
        # Test write-after-write hazard
        #-------------------------------------------------------------

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lhu  x2, 0(x5); \\
            li  x2, 2; \\
            '''
        ],

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lhu  x2, 0(x5); \\
            nop; \\
            li  x2, 2; \\
            '''
        ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x0000000000000ff0, 2, 'tdat2', 0 ],
        [ 0x000000000000f00f, 2, 'tdat3', 1 ],
        [ 0x000000000000ff00, 2, 'tdat1', 2 ],
    ]
    param_src1_bypass = [
        [ 0x0000000000000ff0, 2, 'tdat2', 0 ],
        [ 0x000000000000f00f, 2, 'tdat3', 1 ],
        [ 0x000000000000ff00, 2, 'tdat1', 2 ],       
    ]
    params = { 'test_ld_op': param_ld_op, 
    'test_case': param_case,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .half 0x00ff
tdat2:  .half 0xff00
tdat3:  .half 0x0ff0
tdat4:  .half 0xf00f
'''

    class Case_ld_op_inst(Tdata, Case_ld_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_dest_bypass_inst(Tdata, Case_dest_bypass ):
        pass
    class Case_src1_bypass_inst(Tdata, Case_src1_bypass ):
        pass

class Test_lw(BaseTest_load):
    inst = Lw
    argnames = { 'test_ld_op': ['result', 'offset', 'base'], 
    'test_case': ['testreg', 'correctval', 'code'],
    'test_dest_bypass': ['result', 'offset', 'base', 'nop_cycles'],
    'test_src1_bypass': ['result', 'offset', 'base', 'nop_cycles'],    
    }
    param_ld_op = [
        #-------------------------------------------------------------
        # Basic tests
        #-------------------------------------------------------------

        [ 0x0000000000ff00ff, 0,  'tdat' ],
        [ 0xffffffffff00ff00, 4,  'tdat' ],
        [ 0x000000000ff00ff0, 8,  'tdat' ],
        [ 0xfffffffff00ff00f, 12,  'tdat' ],

        # Test with negative offset

        [ 0x0000000000ff00ff, -12,  'tdat4' ],
        [ 0xffffffffff00ff00, -8,  'tdat4' ],
        [ 0x000000000ff00ff0, -4,  'tdat4' ],
        [ 0xfffffffff00ff00f,  0,  'tdat4' ],       
    ]
    param_case = [
        # Test with a negative base

        [ 'x5', 0x0000000000ff00ff, '''
            la  x1, tdat; \\
            addi x1, x1, -32; \\
            lw x5, 32(x1); \\
            '''
        ],

        # Test with unaligned base

        [ 'x5', 0xffffffffff00ff00, '''
            la  x1, tdat; \\
            addi x1, x1, -3; \\
            lw x5, 7(x1); \\
            '''
        ],

        #-------------------------------------------------------------
        # Test write-after-write hazard
        #-------------------------------------------------------------

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lhu  x2, 0(x5); \\
            li  x2, 2; \\
            '''
        ],

        [ 'x2', 2, '''
            la  x5, tdat; \\
            lw  x2, 0(x5); \\
            nop; \\
            li  x2, 2; \\
            '''
        ],
    ]
    #-------------------------------------------------------------
    # Bypassing tests
    #-------------------------------------------------------------
    param_dest_bypass = [
        [ 0x000000000ff00ff0, 4, 'tdat2', 0 ],
        [ 0xfffffffff00ff00f, 4, 'tdat3', 1 ],
        [ 0xffffffffff00ff00, 4, 'tdat1', 2 ],
    ]
    param_src1_bypass = [
        [ 0x000000000ff00ff0, 4, 'tdat2', 0 ],
        [ 0xfffffffff00ff00f, 4, 'tdat3', 1 ],
        [ 0xffffffffff00ff00, 4, 'tdat1', 2 ],      
    ]
    params = { 'test_ld_op': param_ld_op, 
    'test_case': param_case,
    'test_dest_bypass': param_dest_bypass,
    'test_src1_bypass': param_src1_bypass }

    class Tdata:
        tdata = '''
tdat:
tdat1:  .word 0x00ff00ff
tdat2:  .word 0xff00ff00
tdat3:  .word 0x0ff00ff0
tdat4:  .word 0xf00ff00f
'''

    class Case_ld_op_inst(Tdata, Case_ld_op ):
        pass
    class Case_case_inst(Tdata, Case_case ):
        pass
    class Case_dest_bypass_inst(Tdata, Case_dest_bypass ):
        pass
    class Case_src1_bypass_inst(Tdata, Case_src1_bypass ):
        pass