
import sys

class Inst(dict):
    name = 'unknown'

    def golden(self):
        raise NotImplementedError()