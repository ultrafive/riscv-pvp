# Add New Instructions

To support new instructions, we should create a new `Inst` class in `isa/`
directory.

The new class inherits from the `Inst` class and should override these members
and methods:

 - name : the instruction name string
 - golden(): return how to get dest op from source ops.

```python
# isa/rvi/add.py
from isa.inst import *

class Add(Inst):
    name = 'add'

    def golden(self):
        rd = self['rs1'] + self['rs2']
        return rd
```