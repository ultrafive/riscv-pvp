#!/usr/bin/env python3

from utils.params import *
from isa import *
import re
import yaml
import glob
import os
import textwrap
import argparse
import io
import sys, inspect
from multiprocessing import Pool, Manager, Condition, Value
from string import Template
import shutil
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

# options to configure the test frame
parser.add_argument('--nproc', help='generate elf files on n processes', type=int, default=1)
parser.add_argument('--specs', help='test specs')
parser.add_argument('--cases', help=textwrap.dedent('''\
                                    test case list string or file, for example:
                                    - vsub_vv,addi/test_imm_op/
                                    - cases.list
                                    you can find more examples with option --collect'''), default='')                                    
parser.add_argument('--retry', help='retry last failed cases', action="store_true")
parser.add_argument('--level', help='''put which level of cases together to compile and run:
                                                - inst for one instruction case, 
                                                - type for one test_type cases of one instruction, 
                                                - case for one case in one file''', default="case")
parser.add_argument('--collect', help='just collect the test case to know what cases we can test', action="store_true")
parser.add_argument('--basic-only', help='only run basic test cases for instructions', action="store_true") 
parser.add_argument('--clang', help='path of clang compiler', default='clang')                                               

#options to configure the test CPU
parser.add_argument('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
parser.add_argument('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
parser.add_argument('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
parser.add_argument('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
parser.add_argument('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

args, unknown_args = parser.parse_known_args()
if unknown_args:
    print("Please check your arguments")
    sys.exit(-1)


# to synchronize the generator processes and the main process
manager = Manager()
result_dict = manager.dict()
result_condition = Condition()
result_detail_dict = manager.dict()
tests = Value('L', 0)
fails = Value('L', 0) 


if not args.specs or len(args.specs.split()) == 0:
    # default find the case from specs folder
    specs = ['specs']
else:
    # otherwise find the case from args.specs
    specs = args.specs.split()


collected_case_list = [] # for --collect and generator use this list to generate files
all_case_list = [] # take all cases in specs, used to compute the sum of cases which will be generated
# analyze yml file to find the test cases
for spec in specs:
    if os.path.isdir(spec):
        spec = f'{spec}/**/*.spec.yml'
    # handle every .spec.yml file under spec folder or spec is a .spec.yml file
    for filename in glob.iglob(spec, recursive=True):
        # load information from the yml file 
        stream = open(filename, 'r')
        config = yaml.load(stream, Loader=yaml.SafeLoader)

        for inst, cfg in config.items():
            # don't handle options startswith _
            if inst.startswith('_'):
                continue
            #print(f'{inst}:')

            #print(cfg['templates'])

            # get the value of different options
            attrs = dict()
            attrs['name'] = inst
            attrs['inst'] = globals()[inst.capitalize()]
            attrs['env'] = cfg['env']
            attrs['header'] = cfg['head']
            if 'footer' in cfg:
                attrs['footer'] = cfg['footer']
            if 'tdata' in cfg:
                attrs['tdata'] = cfg['tdata']

            # collect the test configurations
            attrs['test'] = dict()
            for key, params in cfg['cases'].items():
                # get the test_type and arguments from cases option
                [ test_type, *others ] = re.split(r'\s*@\s*', key)
                if len(others) == 2:
                    _args = others[0]
                    _defaults = others[1]
                elif len(others) == 1:
                    _args = others[0]
                    _defaults = ''
                else:
                     _args = ''
                     _defaults = ''

                if not test_type in cfg['templates']:
                    # if no template of this test_type, it's not a test case
                    print(f"can't find the template code for {test_type} of {inst}, Please check!")
                    continue


                # separate the arguments into a list
                if _args:
                    argnames = re.split(r'\s*,\s*', _args)
                    for i in range(len(argnames)):
                        argnames[i] = argnames[i].strip()
                else:
                    argnames = []

                test_info = dict()
                test_info["template"] = cfg['templates'][test_type]
                test_info["args"] = argnames
                if args.basic_only:
                    l = len(params)
                    if l > 4:
                        params = [ c for i, c in enumerate(params) if i in [int(l/4), int(l*2/4), int(l*3/4), l-1]]                
                test_info["params"] = params
                test_info['default'] = _defaults

                if 'check' in cfg.keys() and test_type in cfg['check']:
                    test_info['check'] = cfg['check'][test_type]
                else:
                    test_info['check'] = ''

                attrs['test'][test_type] = test_info

            # take the test cases info into a dict and file to tell users
            if args.level == "inst":
                # just collect the instruction
                collected_case_list.append(inst)

            # collect the instruction, test_type and test_param
            for test_type in attrs['test'].keys():
                if args.level == "type":
                    # collect the instruction and test_type
                    collected_case_list.append(inst+'/'+test_type)                    
                test_info = attrs['test'][test_type]
                attrs['test'][test_type]["case_param"] = dict()
                if test_info["params"]:
                    num = 0
                    for param in test_info["params"]:
                        case_name = ''
                        for i in range(len(test_info["args"])):
                            if i != 0:
                                case_name += '-'
                            case_name += test_info["args"][i]
                        case_name += '_' + str(num)                            
                        attrs['test'][test_type]["case_param"][case_name] = param
                        all_case_list.append(inst+'/'+test_type+'/'+case_name)
                        if args.level == "case":
                            collected_case_list.append(inst+'/'+test_type+'/'+case_name)
                        num += 1
                else:
                    all_case_list.append(inst+'/'+test_type)
                    if args.level == "case":
                        # if npo param, just one case
                        collected_case_list.append(inst+'/'+test_type)

            # define the test function to run tests later
            exec(f'def test_function(self, test_type, test_case): simulate(self, args, test_type, test_case)')
            exec(f'attrs["test_function"] = test_function')
            del globals()['test_function']

            globals()[f'Test_{inst}'] = type(f'Test_{inst}', (object,), attrs)

# log file to tell user what cases there are in the yaml files in this level
with open("log/collected_case.log", 'w') as case_log:
    for case in collected_case_list:
        case_log.write(case)
        case_log.write('\n')

# log file to use in the runner.py to know the cases number it will run
with open("log/all_case.log",'w') as all_log:
    for case in all_case_list:
        all_log.write(case)
        all_log.write('\n')

# call the test_function in the test class to run the test
def run_test( case ):
    stdout = sys.stdout
    stderr = sys.stderr
    output = io.StringIO()
    sys.stdout = output
    sys.stderr = output

    # get the test_instruction、 test_type and test_param by /
    test = case.split('/')
    if len(test) == 1:
        test_instruction = test[0]
        test_type = ''
        test_case = ''
    elif len(test) == 2:
        test_instruction = test[0]
        test_type = test[1]
        test_case = ''  
    else:
        test_instruction = test[0]
        test_type = test[1]
        test_case = test[2]               

    # use the test_function in Test class to run the test
    test_instruction_class = "Test_" + test_instruction
    tic = eval( f'{test_instruction_class}()' )
    tic.test_function( test_type, test_case )

    sys.stdout = stdout
    sys.stderr = stderr

    return output
    
    

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

# translate the numpy array into the data section in the assembly code
def array_data(prefix, k, vv):
    lines = []
    lines.append(f"    .balign {vv.itemsize}")
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

# generate the fields to replace in the template
def generate( tpl, case, inst, case_num, **kw ):
    data = ''
    kw_extra = {}

    for k in kw:
        if isinstance(kw[k], np.ndarray):
            kw_extra[k + '_data'] = "test"+ str(case_num) +"_" + k
            kw_extra[k + '_shape'] = kw[k].shape
            data += array_data(f'test{case_num}', k, kw[k])


    out = inst.golden()
    # this should be removed after all tests compare ndarray on the host
    if isinstance(out, np.ndarray):
        data += array_data(f'test{case_num}', 'rd', out)
        out = f'test{case_num}_rd'

    code = tpl.format_map(dict(num= case_num, name = inst.name, res = out, **kw, **kw_extra))


    if not hasattr(case, 'tdata'):
        case.tdata = ''
    if not hasattr(case, 'footer'):
        case.footer = ''

    content = { "num": case_num, "header":case.header, "env":case.env, "code":code, "data":data, "tdata":case.tdata, "footer":case.footer }


    return content

# compile the test.S
def compile(args, binary, mapfile, dumpfile, source, logfile, **kw):
    cc = f'{args.clang} --target=riscv{args.xlen}-unknown-elf -mno-relax -fuse-ld=lld -march=rv{args.xlen}gv0p10 -menable-experimental-extensions'
    defines = f'-DXLEN={args.xlen} -DVLEN={args.vlen}'
    cflags = '-g -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles'
    incs = '-Ienv/p -Imacros/scalar -Imacros/vector -Imacros/stc'
    linkflags = '-Tenv/p/link.ld'

    cmd = f'{cc} {defines} {cflags} {incs} {linkflags} -Wl,-Map,{mapfile} {source} -o {binary} >> {logfile} 2>&1'
    print(f'# {cmd}\n', file=open(logfile, 'w'))
    ret = os.system(cmd)

    cmd = f'riscv64-unknown-elf-objdump -S -D {binary} > {dumpfile}'
    ret = os.system(cmd)
    return ret

def simulate( test_inst, args, test_type, test_case ):
    #print("test_inst:"+test_inst.name + " test_type:" + test_type + " test_case:"+test_case)
    if test_type == '' and test_case == '':
        # merge the tests of one instruction together

        # file path
        workdir = f'build/{test_inst.name}'
        if os.path.exists(workdir):
            shutil.rmtree(workdir)
        os.makedirs(workdir)        
        source = f'{workdir}/test.S'
        binary = f'{workdir}/test.elf'
        mapfile = f'{workdir}/test.map'
        dumpfile = f'{workdir}/test.dump'
        compile_log = f'{workdir}/compile.log'
        check_golden = f'{workdir}/check_golden.npy'


        # take the header and env into the generated test code
        header = test_inst.header
        env = test_inst.env
        code = ''
        data = ''
        tdata = ''
        footer = ''   

        case_list = []
        num = 0   
        for test_type in test_inst.test.keys():
            test_info = test_inst.test[test_type]
            if test_info["params"]:
                
                for param in test_info["params"]:
                    # get the param
                    param = eval(param) if isinstance(param,str) else param
                    # give a case name
                    case_name = ''
                    for i in range(len(param)):
                        if i != 0:
                            case_name += '-'
                        if isinstance(param[i], np.ndarray):
                            case_name += test_info["args"][i]
                        else:
                            case_name += test_info["args"][i]

                    case_name += '_' + str(num)

                    _kw = ','.join(f'{test_info["args"][i]}=param[{i}]' for i in range(len(param)))
                    default_str = ''
                    if test_info["default"] != '':
                        defaults = re.split(r'\s*,\s*', test_info["default"])
                        
                        for default in defaults:
                            [default_arg, value] = re.split(r'\s*=\s*', default)
                            if test_info["args"].count(value.strip()) > 0:
                                default_str += f'{default_arg}=param[{test_info["args"].index(value.strip())}],'
                            else:
                                default_str += default + ','                     

                    #print(f'test_inst.inst({_kw}, {default_str})')                        
                    inst = eval(f'test_inst.inst({_kw}, {default_str})')
                    golden = inst.golden()
                    # generate the code content
                    content = eval( f'generate( test_info["template"], test_inst, inst, {num}+2,{_kw}, {default_str})' )
                    code += content["code"] + '\n'
                    data += content["data"] + '\n'
                    tdata += content["tdata"] + '\n'
                    footer += content["footer"] + '\n'                   
                    case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'], "golden":golden } )
                    num += 1
            else:
                # if no param, just one case
                inst = test_inst.inst()
                golden = inst.golden()

                #generate the code content
                content = generate( test_info["template"], test_inst, inst, num+2 )
                code += content["code"] + '\n'
                data += content["data"] + '\n'
                tdata += content["tdata"] + '\n'
                footer += content["footer"] + '\n' 
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'], "golden":golden } )
                num += 1

        # generate the test code
        content_all = Template(template).substitute(header=header, env=env, code = code, data = data, tdata=tdata, footer=footer)  
        # save the test code into the source file
        print(content_all, file=open(source, 'w'))   

        # compile the test code 
        ret = compile(args, binary, mapfile, dumpfile, source, compile_log)
        if ret != 0:
            # if failed, set the result as compile failed
            with result_condition:          
                result_dict[test_inst.name] = "compile failed."
                result_detail_dict[test_inst.name] = f'{source} compiled unsuccessfully, please check the compile log file {compile_log}'
            
            with fails.get_lock():
                fails.value += len(case_list)
        
        else:
            np.save(check_golden, case_list)

            with result_condition:          
                result_dict[test_inst.name] = "ok"
                result_detail_dict[test_inst.name] = ""

        with tests.get_lock():
            tests.value += len(case_list)


    elif test_case == '':
        # merge the tests of each test type together 

        header = test_inst.header
        env = test_inst.env

        # file path
        workdir = f'build/{test_inst.name}/{test_type}'
        if os.path.exists(workdir):
            shutil.rmtree(workdir)
        os.makedirs(workdir)        
        source = f'{workdir}/test.S'
        binary = f'{workdir}/test.elf'
        mapfile = f'{workdir}/test.map'
        dumpfile = f'{workdir}/test.dump'
        compile_log = f'{workdir}/compile.log'
        check_golden = f'{workdir}/check_golden.npy'


        # the code field
        code = ''
        data = ''
        tdata = ''
        footer = ''  

        test_info = test_inst.test[test_type]
        case_list = []  
        if test_info["params"]:
            num = 0
            for param in test_info["params"]:
                # get the param
                param = eval(param) if isinstance(param,str) else param

                # give a case name
                case_name = ''
                for i in range(len(param)):
                    if i != 0:
                        case_name += '-'
                    if isinstance(param[i], np.ndarray):
                        case_name += test_info["args"][i]
                    else:
                        case_name += test_info["args"][i]
                case_name += '_' + str(num)

                _kw = ','.join(f'{test_info["args"][i]}=param[{i}]' for i in range(len(param)))

                default_str = ''
                if test_info["default"] != '':
                    defaults = re.split(r'\s*,\s*', test_info["default"])
                    
                    for default in defaults:
                        [default_arg, value] = re.split(r'\s*=\s*', default)
                        if test_info["args"].count(value.strip()) > 0:
                            default_str += f'{default_arg}=param[{test_info["args"].index(value.strip())}],'
                        else:
                            default_str += default + ','

                inst = eval(f'test_inst.inst({_kw}, {default_str})')
                golden = inst.golden()

                # generate the code content
                content = eval( f'generate( test_info["template"], test_inst, inst, num+2, {_kw}, {default_str})' )
                code += content["code"] + '\n'
                data += content["data"] + '\n'
                tdata += content["tdata"] + '\n'
                footer += content["footer"] + '\n'                 
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'], "golden":golden } )
                num += 1
        else:
            # if no param, just one case
            inst = test_inst.inst()
            golden = inst.golden()

            #generate the code content
            content = generate( test_info["template"], test_inst, inst, 2)
            code += content["code"] + '\n'
            data += content["data"] + '\n'
            tdata += content["tdata"] + '\n'
            footer += content["footer"] + '\n'
            case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'], "golden":golden } )

        # generate the test code
        content_all = Template(template).substitute(header=header, env=env, code = code, data = data, tdata=tdata, footer=footer)  
        # save the test code into the source file
        print(content_all, file=open(source, 'w'))   

        # compile the test code 
        ret = compile(args, binary, mapfile, dumpfile, source, compile_log)
        if ret != 0:
            # if failed, set the result as compile failed
            with result_condition:    
                result_dict[f'{test_inst.name}/{test_type}'] = "compile failed."
                result_detail_dict[f'{test_inst.name}/{test_type}'] = f'{source} compiled unsuccessfully, please check the compile log file {compile_log}'

            with fails.get_lock():
                fails.value += len(case_list)
        
        else:
            np.save(check_golden, case_list)

            with result_condition:    
                result_dict[f'{test_inst.name}/{test_type}'] = "ok"
                result_detail_dict[f'{test_inst.name}/{test_type}'] = ''

        with tests.get_lock():
            tests.value += len(case_list)
    

    else:
        # don't merge test case

        header = test_inst.header
        env = test_inst.env

   
        test_info = test_inst.test[test_type]
        # get the param
        test_param = test_info["case_param"][test_case]
        param = eval(test_param) if isinstance(test_param,str) else test_param

        # file path
        workdir = f'build/{test_inst.name}/{test_type}/{test_case}' 
        if os.path.exists(workdir):
            shutil.rmtree(workdir)          
        os.makedirs(workdir)
        source = f'{workdir}/test.S'
        binary = f'{workdir}/test.elf'
        mapfile = f'{workdir}/test.map'
        dumpfile = f'{workdir}/test.dump'
        compile_log = f'{workdir}/compile.log'
        check_golden = f'{workdir}/check_golden.npy'

        _kw = ','.join(f'{test_info["args"][i]}=param[{i}]' for i in range(len(param)))
        default_str = ''
        if test_info["default"] != '':
            defaults = re.split(r'\s*,\s*', test_info["default"])
            
            for default in defaults:
                [default_arg, value] = re.split(r'\s*=\s*', default)
                if test_info["args"].count(value.strip()) > 0:
                    default_str += f'{default_arg}=param[{test_info["args"].index(value.strip())}],'
                else:
                    default_str += default + ','       
        inst = eval(f'test_inst.inst({_kw}, {default_str})')
        golden = inst.golden()

        # generate the code content
        content = eval( f'generate( test_info["template"], test_inst, inst, 2, {_kw}, {default_str})' )
        code = content["code"] + '\n'
        data = content["data"] + '\n'
        tdata = content["tdata"] + '\n'
        footer = content["footer"] + '\n'                 
        case_list =  [{ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{test_case}', "check_str": test_info['check'], "golden": golden } ]

        # generate the test code
        content_all = Template(template).substitute(header=header, env=env, code = code, data = data, tdata=tdata, footer=footer)  
        # save the test code into the source file
        print(content_all, file=open(source, 'w'))   

        # compile the test code 
        ret = compile(args, binary, mapfile, dumpfile, source, compile_log)
        if ret != 0:
            # if failed, set the result as compile failed
            with result_condition:
                result_dict[f'{test_inst.name}/{test_type}/{test_case}'] = "compile failed."
                result_detail_dict[f'{test_inst.name}/{test_type}/{test_case}'] = f'{source} compiled unsuccessfully, please check the compile log file {compile_log}'

            with fails.get_lock():
                fails.value += 1
        
        else:
            np.save(check_golden, case_list)

            with result_condition:
                result_dict[f'{test_inst.name}/{test_type}/{test_case}'] = "ok"
                result_detail_dict[f'{test_inst.name}/{test_type}/{test_case}'] = ''

        with tests.get_lock():
            tests.value += 1     

def generator_error(case):
    with result_condition:
        result_dict[case] = "python run failed."
        result_detail_dict[case] = ''

if __name__ == "__main__":

    os.makedirs('build', exist_ok=True)

    if args.collect:
        print("please look at the contents in the log/collected_case.log")
        sys.exit(0)
      
    
    if args.retry:
        print("retry last failed cases...")
        if os.access('log/generator_report.log', os.R_OK):
            with open('log/generator_report.log') as fp:
                cases = []
                lines = fp.read().splitlines()
                for line in lines:
                    #print(line)
                    if line.startswith('PASS '):
                        continue
                    cases.append(line.replace('FAIL ', ''))
                if len(cases) == 0:
                    print('all pass, retry abort.')
                    sys.exit(0)
        else:
            print('could not retry without last run log.')
            sys.exit(-1)
    else:
        s = lambda l: l.strip()
        f = lambda l: l != '' and not l.startswith('#')
        if os.access(args.cases, os.R_OK):
            with open(args.cases) as fp:
                cases = list(filter(f, map(s, fp.read().splitlines())))
        elif args.cases != '':
            cases = list(filter(f, map(s, args.cases.split(','))))
        else:
            cases = []

    with Pool(processes=args.nproc) as pool:
        ps = []   

        # find the sum of all cases generator will generate to display
        testcase_num = 0
        for testcase in all_case_list:
            if cases and len(cases) > 0:
                for case in cases:
                    if not testcase.startswith(case):                        
                        continue
                    
                    testcase_num += 1
                    break                 
            else:          
                testcase_num += 1

        # progress bar configuration
        progress = Progress(
            TextColumn("[bold blue]{task.fields[name]}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "case_sum:",
            TextColumn("[bold red]{task.total}"),
            "elapsed:",
            TimeElapsedColumn(),
            "remaining:",
            TimeRemainingColumn()
        )

        progress.start()
        task_id = progress.add_task("generation", name = "generation", total=testcase_num, start=True)       
        
        # run tests
        for collect_case in collected_case_list:
            if cases and len(cases) > 0:
                for case in cases:
                    if not collect_case.startswith(case):                        
                        continue
                    
                    res = pool.apply_async(run_test, [ collect_case ], 
                    callback=lambda _: progress.update( task_id, completed = tests.value ), 
                    error_callback=lambda _: generator_error(collect_case)  )
                    # res = run_test(collect_case)
                    ps.append((collect_case, res))   
                    break                 
            else:          
                res = pool.apply_async(run_test, [ collect_case ], 
                callback=lambda _: progress.update( task_id, completed = tests.value ), 
                error_callback=lambda _: generator_error(collect_case)  )
                # res = run_test(collect_case)
                ps.append((collect_case, res))

        failed = 0

        # write the test results into log/generator_report.log
        report = open(f'log/generator_report.log', 'w')
        runner_case = []  
        for case, p in ps:
            ok = True

            p_value = p.get().getvalue()
            # find case result in result_dict
            if result_dict[case] != "ok":
                reason = result_dict[case] + p_value
                ok = False    
            with open(f'build/{case}/generator.log', 'w') as f:
                print(result_dict[case], file=f) 
                print(result_detail_dict[case], file=f) 
                print(p_value, file=f) 

            if not ok:
                failed += 1
                print(f'FAIL {case} - {reason}')
                print(f'FAIL {case} - {reason}', file=report)
            else:
                print(f'PASS {case}', file=report)
                runner_case.append(case)                                                        



        report.close()

        # write the successfully case into the runner_case.log to let the runner to know which cases need to run
        with open("log/runner_case.log", 'w') as runner_log:
            for case in runner_case:
                runner_log.write(case)
                runner_log.write('\n')

        progress.stop()

        if failed == 0:
            print(f'{len(ps)} files generation finish, all pass.( {tests.value} tests )')
            sys.exit(0)
        else:
            print(f'{len(ps)} files generation finish, {failed} failed.( {tests.value} tests, {fails.value} failed )')
            sys.exit(-1)
