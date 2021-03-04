import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veadd_mm import *
from isa.custom.vesub_mm import *

class Case_basic_shapes(BaseCase):
    def template(self, num, name, rd, rs1, rs2, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        return f'TEST_VEXXX_MM_INTERNAL({num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]});'

class BaseTest_vexxx_mm(BaseTest):
    @pytest.mark.parametrize('rs1, rs2', [
        linspace_mm(np.half, 1,  1),
        linspace_mm(np.half, 1, 10),
        linspace_mm(np.half, 10, 1),
    ])
    def test_basic_shapes(self, rs1, rs2):
        simulate(Case_basic_shapes, self.inst, rs1=rs1, rs2=rs2)

class Test_veadd_mm(BaseTest_vexxx_mm):
    inst = Veadd_mm

class Test_vesub_mm(BaseTest_vexxx_mm):
    inst = Vesub_mm
  