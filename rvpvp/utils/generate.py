import os
import re
import shutil
from string import Template
import numpy as np
import jax.numpy as jnp
from .compile import compile
from .utils import copy_to_dtype
from multiprocessing import Manager, Condition, Value

# to synchronize the generator processes and the main process
manager = Manager()
result_dict = manager.dict() # result of test cases
result_detail_dict = manager.dict()   # detail result information of test cases 
result_condition = Condition()  # use this condition to lock the use the result_dict and result_detail_dict
tests = Value('L', 0)    # used to count the amount of test cases which have been generated
fails = Value('L', 0)  # used to count the amount of test cases which generated unsuccessfully


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
        elif vv.dtype == jnp.bfloat16:
            hex_val = x.tobytes()[::-1].hex()
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
def generate_code( tpl, case, inst, case_num, **kw ):
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


def gen_inst_case( args, test_inst ):
    # merge the tests of one instruction together

    # file path
    workdir = f'build/{test_inst.name}'
    if os.path.exists(workdir):
        try:
            shutil.rmtree(workdir)
        except OSError:
            pass
    os.makedirs(workdir, exist_ok=True)       

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
            
            for case_name, param in test_info["case_param"].items():

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
                content = eval( f'generate_code( test_info["template"], test_inst, inst, {num}+2,{_kw}, {default_str})' )
                code += content["code"] + '\n'
                data += content["data"] + '\n'
                tdata += content["tdata"] + '\n'
                footer += content["footer"] + '\n'
                if test_info['check'] != '':                   
                    case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'], "golden_data": copy_to_dtype( golden, np.uint8 ), "golden_dtype": str(golden.dtype) } )
                else:
                    case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'] } )
                num += 1
        else:
            # if no param, just one case
            inst = test_inst.inst()
            golden = inst.golden()

            #generate the code content
            content = generate_code( test_info["template"], test_inst, inst, num+2 )
            code += content["code"] + '\n'
            data += content["data"] + '\n'
            tdata += content["tdata"] + '\n'
            footer += content["footer"] + '\n'
            if test_info['check'] != '':                   
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'], "golden_data": copy_to_dtype( golden, np.uint8 ), "golden_dtype": str(golden.dtype) } )
            else:
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'] } )             
            num += 1

    # generate the test code
    content_all = Template(template).substitute(header=header, env=env, code = code, data = data, tdata=tdata, footer=footer)  
    # save the test code into the source file
    print(content_all, file=open(source, 'w'))

    # compile the test code 
    ret = compile(args.config, binary, mapfile, dumpfile, source, compile_log)
    if ret != 0:
        # if failed, set the result as compile failed
        with result_condition:          
            result_dict[test_inst.name] = "compile failed."
            result_detail_dict[test_inst.name] = f'{source} compiled unsuccessfully, please check the compile log file {compile_log}'
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[test_inst.name] + '\n' + result_detail_dict[test_inst.name] + '\n' )
        
        with fails.get_lock():
            fails.value += len(case_list)
    
    else:
        np.save(check_golden, case_list)

        with result_condition:          
            result_dict[test_inst.name] = "ok"
            result_detail_dict[test_inst.name] = ""
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[test_inst.name] + '\n' + result_detail_dict[test_inst.name] + '\n' )     

    with tests.get_lock():
        tests.value += len(case_list)    

def gen_type_case( args, test_inst, test_type ):
    # merge the tests of each test type together

    header = test_inst.header
    env = test_inst.env
    workdir = f'build/{test_inst.name}/{test_type}'
    if os.path.exists(workdir):
        try:
            shutil.rmtree(workdir)
        except OSError:
            pass
    os.makedirs(workdir, exist_ok=True)       
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
        for case_name, param in test_info["case_param"].items():

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
            content = eval( f'generate_code( test_info["template"], test_inst, inst, num+2, {_kw}, {default_str})' )
            code += content["code"] + '\n'
            data += content["data"] + '\n'
            tdata += content["tdata"] + '\n'
            footer += content["footer"] + '\n'
            if test_info['check'] != '':                   
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'], "golden_data": copy_to_dtype( golden, np.uint8 ), "golden_dtype": str(golden.dtype) } )
            else:
                case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{case_name}', "check_str": test_info['check'] } )                             
            num += 1
    else:
        # if no param, just one case
        inst = test_inst.inst()
        golden = inst.golden()

        #generate the code content
        content = generate_code( test_info["template"], test_inst, inst, 2)
        code += content["code"] + '\n'
        data += content["data"] + '\n'
        tdata += content["tdata"] + '\n'
        footer += content["footer"] + '\n'
        if test_info['check'] != '':                   
            case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'], "golden_data": copy_to_dtype( golden, np.uint8 ), "golden_dtype": str(golden.dtype) } )
        else:
            case_list.append({ "no": content["num"], "name": f'{test_inst.name}/{test_type}', "check_str": test_info['check'] } )

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
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[f'{test_inst.name}/{test_type}'] + '\n' + result_detail_dict[f'{test_inst.name}/{test_type}'] + '\n' )

        with fails.get_lock():
            fails.value += len(case_list)
    
    else:
        np.save(check_golden, case_list)

        with result_condition:    
            result_dict[f'{test_inst.name}/{test_type}'] = "ok"
            result_detail_dict[f'{test_inst.name}/{test_type}'] = ''
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[f'{test_inst.name}/{test_type}'] + '\n' + result_detail_dict[f'{test_inst.name}/{test_type}'] + '\n' )            

    with tests.get_lock():
        tests.value += len(case_list)

def gen_case( args, test_inst, test_type, test_case ):
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
        try:
            shutil.rmtree(workdir)
        except OSError:
            pass
    os.makedirs(workdir, exist_ok=True)

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
    content = eval( f'generate_code( test_info["template"], test_inst, inst, 2, {_kw}, {default_str})' )
    code = content["code"] + '\n'
    data = content["data"] + '\n'
    tdata = content["tdata"] + '\n'
    footer = content["footer"] + '\n'
    if test_info['check'] != '':                 
        case_list =  [{ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{test_case}', "check_str": test_info['check'], "golden_data": copy_to_dtype( golden, np.uint8 ), "golden_dtype": str(golden.dtype) } ]
    else:
        case_list =  [{ "no": content["num"], "name": f'{test_inst.name}/{test_type}/{test_case}', "check_str": test_info['check'] }]

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
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[f'{test_inst.name}/{test_type}/{test_case}'] + '\n' + result_detail_dict[f'{test_inst.name}/{test_type}/{test_case}'] + '\n' )

        with fails.get_lock():
            fails.value += 1
    
    else:
        np.save(check_golden, case_list)

        with result_condition:
            result_dict[f'{test_inst.name}/{test_type}/{test_case}'] = "ok"
            result_detail_dict[f'{test_inst.name}/{test_type}/{test_case}'] = ''
            with open(f'{workdir}/generator.log', 'w') as f:
                f.write( result_dict[f'{test_inst.name}/{test_type}/{test_case}'] + '\n' + result_detail_dict[f'{test_inst.name}/{test_type}/{test_case}'] + '\n' )            

    with tests.get_lock():
        tests.value += 1

def generate( test_inst, args, test_type, test_case ):

    #print("test_inst:"+test_inst.name + " test_type:" + test_type + " test_case:"+test_case)
    if test_type == '' and test_case == '':

        gen_inst_case( args, test_inst )


    elif test_case == '':
        
        gen_type_case( args, test_inst, test_type )    

    else:

        gen_case( args, test_inst, test_type, test_case )