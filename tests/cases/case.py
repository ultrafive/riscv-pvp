from isa.inst import *

class BaseTest:
    inst = Inst

class BaseCase:
    def template(self, num, name, res, *args ):
        raise NotImplementedError()

    def mem_diff(self, golden, results):
        return True

    def results(self):
        return {}