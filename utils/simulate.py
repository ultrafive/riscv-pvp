
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
def compile(args, binary, mapfile, dumpfile, source, logfile, **kw):
    cc = f'{args.clang} --target=riscv{args.xlen}-unknown-elf -mno-relax -fuse-ld=lld -march=rv{args.xlen}gv0p10 -menable-experimental-extensions'
    defines = f'-DXLEN={args.xlen} -DVLEN={args.vlen}'
    cflags = '-g -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles'
    incs = '-Ienv/p -Imacros/scalar -Imacros/vector -Imacros/stc'
    linkflags = '-Tenv/p/link.ld'

    cmd = f'{cc} {defines} {cflags} {incs} {linkflags} -Wl,-Map,{mapfile} {source} -o {binary} > {logfile} 2>&1'
    ret = os.system(cmd)
    allure.attach(cmd, 'command line', attachment_type=allure.attachment_type.TEXT)
    allure.attach.file(logfile, 'compile log', attachment_type=allure.attachment_type.TEXT)


    cmd = f'riscv64-unknown-elf-objdump -S -D {binary} > {dumpfile}'
    ret = os.system(cmd)
    assert ret == 0

@allure.step
def run(args, memfile, binary, logfile, res_file, **kw):
    sim = f'{args.spike} --isa=rv{args.xlen}gcv --varch=vlen:{args.vlen},elen:{args.elen},slen:{args.slen}'

    cmd = f'{sim} +signature={res_file} +signature-granularity={32} {binary} > {logfile} 2>&1'
    ret = os.system(cmd)
    allure.attach(cmd, 'command line', attachment_type=allure.attachment_type.TEXT)
    allure.attach.file(logfile, 'run log', attachment_type=allure.attachment_type.TEXT)
    assert ret == 0

@allure.step
def readmem(memfile, symbol):
    pass


@allure.step
def generate(source, tpl, case, inst, **kw):

    data = ''
    kw_extra = {}
    for k in kw:
        if isinstance(kw[k], np.ndarray):
            kw_extra[k + '_data'] = "test_" + k
            kw_extra[k + '_shape'] = kw[k].shape
            data += array_data(f'test', k, kw[k])


    out = inst.golden()
    # this should be removed after all tests compare ndarray on the host
    if isinstance(out, np.ndarray):
        data += array_data(f'test', 'rd', out)
        out = "test_rd"

    code = tpl.format_map(dict(num= 2, name = inst.name, res = out, **kw, **kw_extra))

    if not hasattr(case, 'tdata'):
        case.tdata = ''
    if not hasattr(case, 'footer'):
        case.footer = ''
    content = Template(template).substitute(header=case.header, env=case.env, code = code, data = data, tdata=case.tdata, footer=case.footer)
    print(content,  file=open(source, 'w'))
    allure.attach.file(source, 'source file', attachment_type=allure.attachment_type.TEXT)

def from_txt(fpath, ebyte, size, dtype):
    result = []
    with open(fpath) as file:
        for line in file:
            line = line.rstrip()
            if ebyte != 0.1:
                for no in range(int(32/ebyte)):
                    if no == 0:
                        str = line[-2*ebyte:]
                    else:
                        str = line[-(no+1)*2*ebyte:-no*2*ebyte]
                    num = int( str, 16 )
                    result.append( num )
            else:
                for no in range(64):
                    str = line[ 63-no ]
                    num = int(str, 16)
                    result.append( num >> 0 & 1 )
                    result.append( num >> 1 & 1 )
                    result.append( num >> 2 & 1 )
                    result.append( num >> 3 & 1 )

            if len(result) >= size:
                break

    result = result[:size]
    
    if ebyte == 0.1:
        ebyte = 1
        
    data = np.array(result, dtype='uint%d' % (ebyte*8))
    data.dtype = dtype
    return data

def diff_to_txt(a, b, filename):
    a = a.reshape(-1)
    b = b.reshape(-1)
    ah = a.copy()
    ah.dtype = f'uint{a.itemsize * 8}'
    bh = b.copy()
    bh.dtype = f'uint{b.itemsize * 8}'

    w = a.itemsize * 2
    if a.dtype == np.float16 or a.dtype == np.float32 or a.dtype == np.float64:
        t = 'f'
    else:
        t = 'd'

    with open(filename, 'w') as file:
        for i in range(a.shape[0]):
            if a[i] == b[i] or (np.isnan(a[i]) and np.isnan(b[i])):
                print(f'%3d: %{w+4}{t}(%0{w}x), %{w+4}{t}(%0{w}x)' % (i, a[i], ah[i], b[i], bh[i]), file=file)
            else:
                print(f'%3d: %{w+4}{t}(%0{w}x), %{w+4}{t}(%0{w}x), mismatch' % (i, a[i], ah[i], b[i], bh[i]), file=file)


@allure.step
def check(res_file, golden, check_str, workdir):
    itemsize = golden.itemsize
    size = golden.size
    dtype = golden.dtype

    if golden.dtype == np.bool_:
        itemsize = 0.1

    result = from_txt(res_file, itemsize, size, dtype)

    result.dtype = golden.dtype
    result = result.reshape( golden.shape )
    diff_to_txt(golden, result, f'{workdir}/check.data')
    allure.attach.file(f'{workdir}/check.data', f'check result', attachment_type=allure.attachment_type.TEXT)
    assert eval(check_str)

@allure.step
def diff(args, run_mem, binary, res_file, golden, workdir):
    if not isinstance(golden, np.ndarray):
        return

    itemsize = golden.itemsize
    size = golden.size
    dtype = golden.dtype
    gold = from_txt(res_file, itemsize, size, dtype)

    sims = { 'vcs': args.vcs, 'verilator': args.verilator }
    for k, sim in sims.items():
        if sim == None:
            continue
        options = f'+signature={workdir}/{k}.sig +signature-granularity={32}'
        if k == 'vcs' and args.fsdb:
            options += f' +permissive +fsdbfile={workdir}/test.fsdb +permissive-off'

        cmd = f'{sim} {options} {binary} > {workdir}/{k}.log 2>&1'
        ret = os.system(cmd)
        allure.attach(cmd, f'{k} command line', attachment_type=allure.attachment_type.TEXT)
        allure.attach.file(f'{workdir}/{k}.log', f'{k} log', attachment_type=allure.attachment_type.TEXT)
        assert ret == 0

        data = from_txt(f'{workdir}/{k}.sig', itemsize, size, dtype)
        diff_to_txt(gold, data, f'{workdir}/diff-{k}.data')
        allure.attach.file(f'{workdir}/diff-{k}.data', f'{k} diff', attachment_type=allure.attachment_type.TEXT)
        assert np.array_equal(gold, data, equal_nan=True)


def simulate(testcase, args, template, check_str, **kw):
    workdir = os.environ.get("WORKDIR")
    instclass = testcase.inst

    source = f'{workdir}/test.S'
    binary = f'{workdir}/test.elf'
    mapfile = f'{workdir}/test.map'
    dumpfile = f'{workdir}/test.dump'
    compile_log = f'{workdir}/compile.log'
    run_log = f'{workdir}/spike.log'
    run_mem = f'{workdir}/run.mem'
    res_file = f'{workdir}/spike.sig'

    inst = instclass(**kw)
    golden = inst.golden()

    generate(source, template, testcase, inst, **kw)
    compile(args, binary, mapfile, dumpfile, source, compile_log, **kw)
    run(args, run_mem, binary, run_log, res_file, **kw)
    if check_str != '0':
        check(res_file, golden, check_str, workdir)
    diff(args, run_mem, binary, res_file, golden, workdir)
