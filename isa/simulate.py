
from string import Template
import os
import numpy as np

case_num = 0

template = '''
#include "riscv_test.h"
#include "test_macros.h"
#include "vexxx_mm.h"

RVTEST_RV32STC
RVTEST_CODE_BEGIN
    $code
    TEST_PASSFAIL

RVTEST_CODE_END

    .data
RVTEST_DATA_BEGIN

    TEST_DATA
    $data
RVTEST_DATA_END
'''

def array_data(prefix, k, vv):
    lines = []
    lines.append(f"    .align {vv.itemsize}")
    lines.append(prefix + "_" + k + ":")
    if vv.size == 0:
        return ''
    for x in np.nditer(vv):
        hex_val = x.byteswap().tobytes().hex()
        if vv.dtype == np.float16:
            lines.append(f"    .half   0x{hex_val} // {x}")
        elif vv.dtype == np.float32:
            lines.append(f"    .word   0x{hex_val} // {x}")
        elif vv.dtype == np.float64:
            lines.append(f"    .dword  0x{hex_val} // {x}")
        elif vv.dtype == np.int8 or vv.dtype == np.byte or vv.dtype == np.ubyte:
            lines.append(f"    .byte   0x{hex_val} // {x}")
        elif vv.dtype == np.int16 or vv.dtype == np.short or vv.dtype == np.ushort:
            lines.append(f"    .half   0x{hex_val} // {x}")
        elif vv.dtype == np.int32 or vv.dtype == np.intc or vv.dtype == np.uintc:
            lines.append(f"    .word   0x{hex_val} // {x}")
        elif vv.dtype == np.int64 or vv.dtype == np.int or vv.dtype == np.uint:
            lines.append(f"    .dword  0x{hex_val} // {x}")
    return '\n'.join(lines) + '\n'

def generate_source(source, case, inst, **kw):
   

    data = ''
    kw_extra = {}
    for k in kw:
        if isinstance(kw[k], np.ndarray):
            kw_extra[k + '_data'] = "test_" + k
            kw_extra[k + '_shape'] = kw[k].shape
            data += array_data(f'test', k, kw[k])
    print(data)

    args = list({**kw, **kw_extra}.values())

    out = inst.golden()
    if isinstance(out, np.ndarray):
        data += array_data(f'test', 'rd', out)
        out = "test_rd"
    code = case.template(2, inst.name, out, *args)

    content = Template(template).substitute(code = code, data = data)
    print(content,  file=open(source, 'w'))

CC = 'clang'
ARCH_FLAGS = '-march=rv32g -mabi=ilp32'
TARGET_FLAGS = '--target=riscv32npu -static -nostdlib -nostartfiles'
INCS = '-I env/b -Imacros/scalar -Imacros/vector -Imacros/stc'
LINKFLAGS = '-Tenv/b/link.ld'

SIM = 'spike'

def compile(binary, mapfile, source, **kw):
    cmd = f'{CC} {ARCH_FLAGS} {TARGET_FLAGS} {INCS} {LINKFLAGS} -Wl,-Map,{mapfile} {source} -o {binary}'
    assert os.system(cmd) == 0

def run(memfile, logfile, binary, **kw):
    cmd = f'{SIM} {binary} > {logfile} 2>&1'
    assert os.system(cmd) == 0

def readmem(memfile, symbol):
    pass

def diff(resmap, golden, memfile):
    for symbol in resmap:
        assert golden[symbol] == readmem(memfile, symbol)

def simulate(testcase, caseclass, **kw):
    workdir = testcase.workdir
    instclass = testcase.inst

    source = f'{workdir}/test.S'
    binary = f'{workdir}/test.elf'
    mapfile = f'{workdir}/test.map'
    logfile = f'{workdir}/test.log'
    memfile = f'{workdir}/test.mem'

    inst = instclass(**kw)
    golden = inst.golden()

    case = caseclass()
    resmap = case.results()

    generate_source(source, case, inst, **kw)
    compile(binary, mapfile, source, **kw)
    run(memfile, logfile, binary, **kw)

    diff(resmap, golden, memfile)
