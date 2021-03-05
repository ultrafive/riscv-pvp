import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.rvi.addi import *
from isa.rvi.ori import *

class Case_imm_op(BaseCase):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_OP( {num}, {name}, {res}, {val1}, {imm} );'
class Case_src1_eq_dest(BaseCase):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_SRC1_EQ_DEST( {num}, {name}, {res}, {val1}, {imm} );'

class Case_dest_bypass(BaseCase):
    def template(self, num, name, res, val1, imm, nop_cycles ):
        return f'TEST_IMM_DEST_BYPASS( {num}, {nop_cycles}, {name}, {res}, {val1}, {imm} );'

class Case_src1_bypass(BaseCase):
    def template(self, num, name, res, val1, imm, nop_cycles ):
        return f'TEST_IMM_SRC1_BYPASS( {num}, {nop_cycles}, {name}, {res}, {val1}, {imm} );'

class Case_imm_zerosrc1(BaseCase):
    def template(self, num, name, res, val1, imm ):
        return f'TEST_IMM_ZEROSRC1( {num}, {name}, {res}, {imm} );'

class BaseTest_rvi_imm(BaseTest):
    @pytest.mark.parametrize('rs1, imm', [
        ( 0x00000000, 0x000 ),
        ( 0x00000001, 0x001 ),
        ( 0x00000003, 0x007 ),
    ])
    def test_arithmetic(self, rs1, imm):
        simulate(self, Case_imm_op, rs1=rs1, imm=imm)

    def test_cov(self, workdir):
        for x in range(2):
            for y in range(2):
                simulate(self, Case_imm_op, rs1=x, imm=y)

    @pytest.mark.parametrize('rs1, imm', [
        ( 13, 11 ),
    ])
    def test_src1_eq_dest(self, rs1, imm):
        simulate(self, Case_src1_eq_dest, rs1=rs1, imm=imm)

    @pytest.mark.parametrize('rs1, imm, nop_cycles', [
        ( 13, 11 , 0 ),
        ( 13, 10 , 1 ),
        ( 13,  9 , 2 ),
    ])
    def test_dest_bypass(self, rs1, imm, nop_cycles):
        simulate(self, Case_dest_bypass, rs1=rs1, imm=imm, nop_cycles=nop_cycles)

    @pytest.mark.parametrize('rs1, imm, nop_cycles', [
        ( 13, 11 , 0 ),
        ( 13, 10 , 1 ),
        ( 13,  9 , 2 ),
    ])
    def test_src1_bypass(self, rs1, imm, nop_cycles):
        simulate(self, Case_src1_bypass, rs1=rs1, imm=imm, nop_cycles=nop_cycles)

    @pytest.mark.parametrize('imm', [
        ( 32 ),
        ( 50 ),
    ])
    def test_zerosrc1(self, imm):
        simulate(self, Case_imm_zerosrc1, rs1=0, imm=imm)
        
class Test_addi(BaseTest_rvi_imm):
    inst = Addi

class Test_ori(BaseTest_rvi_imm):
    inst = Ori
  