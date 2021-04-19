
from string import Template
import os
import numpy as np
import allure

case_num = 0

template = '''
#include "riscv_test.h"
#include "test_macros.h"
$header

$env
RVTEST_CODE_BEGIN
    $code
    TEST_PASSFAIL

    TEST_EXCEPTION_HANDLER

RVTEST_CODE_END

    .data
RVTEST_DATA_BEGIN

    TEST_DATA
    .subsection 1
    $data
    $tdata
RVTEST_DATA_END
$footer
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

@allure.step
def generate(source, case, inst, **kw):

    data = ''
    kw_extra = {}
    for k in kw:
        if isinstance(kw[k], np.ndarray):
            kw_extra[k + '_data'] = "test_" + k
            kw_extra[k + '_shape'] = kw[k].shape
            data += array_data(f'test', k, kw[k])

    args = list({**kw, **kw_extra}.values())

    out = inst.golden()
    if isinstance(out, np.ndarray):
        data += array_data(f'test', 'rd', out)
        out = "test_rd"
    code = case.template(2, inst.name, out, *args)

    content = Template(template).substitute(header=case.header, env=case.env, code = code, data = data, tdata=case.tdata, footer=case.footer)
    print(content,  file=open(source, 'w'))
    allure.attach.file(source, 'source file', attachment_type=allure.attachment_type.TEXT)
'''
CC = 'clang'
ARCH_FLAGS = ''
TARGET_FLAGS = '--target=riscv32 -mcpu=npu-v1 -static -nostdlib -nostartfiles'
INCS = '-Ienv/b -Imacros/scalar -Imacros/vector -Imacros/stc'
LINKFLAGS = '-Tenv/b/link.ld'
'''

CC = 'clang --target=riscv64-unknown-elf -mno-relax -fuse-ld=lld'
ARCH_FLAGS = '-march=rv64gv0p10 -menable-experimental-extensions -DXLEN=64 -DVLEN=1024'
TARGET_FLAGS = '-g -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles'
INCS = '-Ienv/p -Imacros/scalar -Imacros/vector -Imacros/stc'
LINKFLAGS = '-Tenv/p/link.ld'

SIM = 'spike --isa=rv64gcv'
VARCH = '--varch=vlen:1024,elen:64,slen:1024'

@allure.step
def compile(binary, mapfile, source, logfile, **kw):
    cmd = f'{CC} {ARCH_FLAGS} {TARGET_FLAGS} {INCS} {LINKFLAGS} -Wl,-Map,{mapfile} {source} -o {binary} > {logfile} 2>&1'
    ret = os.system(cmd)
    allure.attach(cmd, 'command line', attachment_type=allure.attachment_type.TEXT)
    allure.attach.file(logfile, 'compile log', attachment_type=allure.attachment_type.TEXT)
    assert ret == 0

@allure.step
def run(memfile, binary, logfile, res_file, **kw):
    cmd = f'{SIM} {VARCH} +signature={res_file} {binary} > {logfile} 2>&1'
    ret = os.system(cmd)
    allure.attach(cmd, 'command line', attachment_type=allure.attachment_type.TEXT)
    allure.attach.file(logfile, 'run log', attachment_type=allure.attachment_type.TEXT)
    assert ret == 0

@allure.step
def readmem(memfile, symbol):
    pass

@allure.step
def diff(resmap, golden, memfile):
    for symbol in resmap:
        assert golden[symbol] == readmem(memfile, symbol)

def simulate(testcase, caseclass, **kw):
    workdir = testcase.workdir
    instclass = testcase.inst

    source = f'{workdir}/test.S'
    binary = f'{workdir}/test.elf'
    mapfile = f'{workdir}/test.map'
    compile_log = f'{workdir}/compile.log'
    run_log = f'{workdir}/run.log'
    run_mem = f'{workdir}/run.mem'

    inst = instclass(**kw)
    golden = inst.golden()

    case = caseclass()
    resmap = case.results()

    generate(source, case, inst, **kw)
    compile(binary, mapfile, source, compile_log, **kw)
    run(run_mem, binary, run_log, **kw)

    diff(resmap, golden, run_mem)

@allure.step
def generate2(source, tpl, case, inst, **kw):

    data = ''
    kw_extra = {}
    for k in kw:
        if isinstance(kw[k], np.ndarray):
            kw_extra[k + '_data'] = "test_" + k
            kw_extra[k + '_shape'] = kw[k].shape
            data += array_data(f'test', k, kw[k])


    # out = inst.golden()
    # if isinstance(out, np.ndarray):
    #     data += array_data(f'test', 'rd', out)
    #     out = "test_rd"

    code = tpl.format_map(dict(num= 2, name = inst.name, res = 0, **kw, **kw_extra))

    if not hasattr(case, 'tdata'):
        case.tdata = ''
    if not hasattr(case, 'footer'):
        case.footer = ''
    content = Template(template).substitute(header=case.header, env=case.env, code = code, data = data, tdata=case.tdata, footer=case.footer)
    print(content,  file=open(source, 'w'))
    allure.attach.file(source, 'source file', attachment_type=allure.attachment_type.TEXT)

@allure.step
def diff2(res_file, golden, diff_str):
    itemsize = golden.itemsize
    size = golden.size
    result = []
    with open(res_file) as file:
        for line in file:
            line = line.rstrip()
            for no in range(int(16/itemsize)):
                if no == 0:
                    str = line[-2*itemsize:]
                else:
                    str = line[-(no+1)*2*itemsize:-no*2*itemsize]
                num = int( str, 16 )
                result.append( num )
            if len(result) >= size:
                break
    result = result[:size]
    result = np.array(result, dtype='uint%d' % (itemsize*8))
    result.dtype = golden.dtype
    result = result.reshape( golden.shape )
    print(golden)  
    print(result)
    assert eval(diff_str)

def simulate2(testcase, template, diff_str, **kw):
    workdir = testcase.workdir
    instclass = testcase.inst

    source = f'{workdir}/test.S'
    binary = f'{workdir}/test.elf'
    mapfile = f'{workdir}/test.map'
    compile_log = f'{workdir}/compile.log'
    run_log = f'{workdir}/run.log'
    run_mem = f'{workdir}/run.mem'
    res_file = f'{workdir}/res.txt'

    inst = instclass(**kw)
    golden = inst.golden()

    generate2(source, template, testcase, inst, **kw)
    compile(binary, mapfile, source, compile_log, **kw)
    run(run_mem, binary, run_log, res_file, **kw)
    if diff_str != '0':
        diff2(res_file, golden, diff_str)
