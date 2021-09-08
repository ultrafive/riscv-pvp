from ...isa.inst import *

class Vsetvl(Inst):
    name = 'vsetvl'
    # vsetvl rd, rs1, rs2 # rd = new vl, rs1 = AVL, rs2 = new vtype value   
    def golden(self):
        return 0

class Vsetvli(Vsetvl):
    name = 'vsetvli'
    # vsetvli rd, rs1, vtypei # rd = new vl, rs1 = AVL, vtypei = new vtype setting     

class Vsetivli(Vsetvl):
    name = 'vsetivli'  
    # vsetivli rd, uimm, vtypei # rd = new vl, uimm = AVL, vtypei = new vtype setting  
