#!/usr/bin/env python3
from utils.params import *
from utils.generate import generate, result_dict, result_detail_dict, result_condition, tests, fails
from isa import *
import jax.numpy as jnp
import re
import yaml
import glob
import os
import textwrap
import argparse
import io
import sys, inspect
from multiprocessing import Pool
import types
import inspect
import time
import traceback
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)



def parse_argument():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    # options to configure the test frame
    parser.add_argument('--config', help='config yaml file', default='config/prod.yml')
    parser.add_argument('--nproc', '-n', help='generate elf files on n processes', type=int, default=1)
    parser.add_argument('--level', '-l', help='''put which level of cases together to compile and run:
                                                    - inst for one instruction case, 
                                                    - type for one test_type cases of one instruction, 
                                                    - case for one case in one file''', default="case")
  

    parser.add_argument('--specs', '-s', help='test specs')
    parser.add_argument('--cases', '-c', help=textwrap.dedent('''\
                                        test case list string or file, for example:
                                        - vsub_vv,addi/test_imm_op/
                                        - cases.list
                                        you can find more examples with option --collect'''), default='')                                    

    parser.add_argument('--collect', help='just collect the test case to know what cases we can test', action="store_true")
    parser.add_argument('--little', help='only run at most 4 test cases for each test type of each instruction', action="store_true") 
    parser.add_argument('--basic', '-b', help='run basic tests of basic_cases test data in yml for regression.', action='store_true')
    parser.add_argument('--random', '-r', help='run random tests of random_cases test data in yml', action='store_true')
    parser.add_argument('--seed', help="set random seed for random functions of each spec yaml", type=int, default=3428)
    parser.add_argument('--rtimes', help="set random cases generation times", type=int, default=1)    
    parser.add_argument('--retry', help='retry last failed cases', action="store_true") 

    parser.add_argument('--failing-info', '-fi', help="print the failing info into the screen, rather than into the log/generator_report.log.", action="store_true")                                              
    parser.add_argument('--param-info', '-pi', help="print params information into log/params.yaml of cases collected.", action = "store_true")

    args, unknown_args = parser.parse_known_args()
    
    # if there are wrong arguments, print and exit
    if unknown_args:
        print("Please check your arguments(%s)." % unknown_args)
        sys.exit(-1)
    
    return args

def get_config_info(args):
    config_file = args.config
    # analyse the env.yaml to get compile info
    with open(config_file, 'r' ) as f_config:
        config = yaml.load(f_config, Loader=yaml.SafeLoader)
        globals()["xlen"] = config["processor"]['xlen']
        globals()["flen"] = config["processor"]['flen']
        globals()["vlen"] = config["processor"]['vlen']
        globals()["elen"] = config["processor"]['elen']
        globals()["slen"] = config["processor"]['slen']
        globals()["path"] = config["compile"]['path']
        globals()["cc"] = eval(config["compile"]['cc'])
        globals()["defines"] = eval(config["compile"]['defines'])
        globals()["cflags"] = config["compile"]['cflags']
        globals()["incs"] = config["compile"]['incs']
        globals()["linkflags"] = config["compile"]['linkflags']
        globals()["compile_cmd"] = f'{cc} {defines} {cflags} {incs} {linkflags}'
        globals()["objdump_cmd"] = config["compile"]["objdump"]
        globals()["is_objdump"] = config["compile"]["is_objdump"]
        globals()["readelf"] = config["compile"]['readelf']
        globals()["config"] = config
        args.compile_config = { "compile_cmd": compile_cmd, "objdump_cmd": objdump_cmd, "is_objdump": is_objdump }

# find the params for matrix cases
def search_matrix(arg_names, vals, no, params, locals_dict, **kwargs):
    if no == len(vals):#when all arguments in kwargs
        params.append(kwargs)
        return

    merge_dict = { **locals_dict, **kwargs }
    # define the arguments in kwargs to help compute next param
    for key, val in merge_dict.items():
        if isinstance(val,str):
            exec(f'{key}="{val}"')
        elif isinstance(val, np.ndarray):
            val_str = val.tobytes()
            exec(f'{key}=np.reshape( np.frombuffer( val_str, dtype=jnp.{val.dtype}), {val.shape}) ')
        elif inspect.isfunction( merge_dict[key] ):
            exec(f'{key}=merge_dict["{key}"]')
        else:
            exec(f'{key}={val}')

    # just to unify the handle process
    if not isinstance(vals[no], list):
        vals[no] = [vals[no]]

    for val in vals[no]:
        try:
            vals_next = eval(val) if isinstance(val,str) else val
        except NameError:# when the string is jsut a string and can't be run
            vals_next = val
        
        # in case of the string is same as built-in function and type
        if isinstance(vals_next,types.BuiltinFunctionType) or inspect.isclass(vals_next):
            vals_next = val
        
        # just to unify the handle process
        if not isinstance(vals_next, list):
            vals_next=[vals_next]
        
        for val_el in vals_next:
            # take this argument into kwargs and continue to search next argument 
            kwargs[arg_names[no]] = val_el
            search_matrix(arg_names, vals, no+1, params, locals_dict, **kwargs)

    # get the params list from dictionary
    if no == 0:
        params_yml = []

        for param_dict in params:
            vals = []
            for arg in arg_names:
                vals.append(param_dict[arg])
            
            params_yml.append(vals)
        
        return params_yml

def cases_gen( args, filename, inst, cases_dict, templates, check_dict, collected_case_list, collected_case_num_list, param_dict  ):
    
    test_dict = dict()

    for key, params in cases_dict.items():

        # the default input mode for cases argument is common, test_case @ a, b ,c:
        param_mode = 'common'

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

            # the matrix mode in cases
            if isinstance(params, dict) and 'matrix' in params:
                param_mode = 'matrix'

        if not test_type in templates:
            # if no template of this test_type, it's not a test case
            print(f"can't find the template code for {test_type} of {inst} in {filename}, Please check!")
            continue

        # use test_info to save the test information of one type of test cases
        test_info = dict()

        test_info["template"] = templates[test_type]

        if param_mode == 'common':
            # test_type @ xx,xx,xx@ xx=xx

            # must not use the matrix key with @ ...@ ..=..
            if isinstance(params, dict) and 'matrix' in params:
                print(f"@ argument list can't be used with matrix in params.-{test_type} of {inst} in {filename}")
                continue

            # separate the arguments into a list
            if _args:
                argnames = re.split(r'\s*,\s*', _args)
                for i in range(len(argnames)):
                    argnames[i] = argnames[i].strip()
            else:
                argnames = []

            test_info["args"] = argnames

            if isinstance(params, dict) and 'setup' in params:
                # use argument list and params_yml in setup to get the params
                if _args == '':
                    print(f"setup needs to be used with argument list, please check.-{test_type} of {inst} in {filename}")
                    continue
                
                # if there is the variable params_yml before, delete it first.
                if 'params_yml' in globals() or 'params_yml' in locals():
                    del params_yml

                if args.random:
                    rtimes = args.rtimes
                else:
                    rtimes = 1
                params_yml = []
                while rtimes >  0:
                    rtimes -= 1
                    locals_dict = dict()
                    exec(params["setup"], globals(), locals_dict)
                    if not 'params_yml' in locals_dict:
                        print(f"no params_yml in setup, please check.-{test_type} of {inst} in {filename}")
                        continue
                    else:
                        params_yml.extend( locals_dict['params_yml'] )
            
            else:                
                if args.random:
                    rtimes = args.rtimes
                else:
                    rtimes = 1
                params_yml = []
                while rtimes >  0:
                    rtimes -= 1
                    params_yml.extend( params )

        elif param_mode == 'matrix':
            if args.random:
                rtimes = args.rtimes
            else:
                rtimes = 1
            params_yml = []
            # get argument names and params
            argnames = list(params['matrix'].keys())
            test_info["args"] = argnames
            vals = list(params['matrix'].values())            
            while rtimes >  0:
                rtimes -= 1

                locals_dict = {}
                # setup string is the preparatory work for matrix
                if 'setup' in params:
                    exec(params['setup'], globals(), locals_dict)

                                
                # compute the params values
                params_dict_yml = []            
                params_yml.extend( search_matrix(argnames, vals, 0, params_dict_yml, locals_dict) )

        else:
            continue

        if args.little:
            l = len(params_yml)                   
            if l > 4:
                params_yml = [ c for i, c in enumerate(params_yml) if i in [int(l/4), int(l*2/4), int(l*3/4), l-1] ]
        test_info["params"] = params_yml

        test_info['default'] = _defaults

        if test_type in check_dict:
            test_info['check'] = check_dict[test_type]
        else:
            test_info['check'] = ''

        if args.param_info:
            param_dict[inst][test_type] = dict()

        if args.level == "type":
            # collect the instruction and test_type
            collected_case_list.append(inst+'/'+test_type)
            collected_case_num_list.append(0)

        # compute params and set the case name      
        test_info["case_param"] = dict()
        if test_info["params"]:
            num = 0         
            for param in test_info["params"]:
                
                # compute params value
                param = eval(param) if isinstance(param, str) else param

                # set the case name
                case_name = f'test{num}_'
                for i in range(len(test_info["args"])):
                    if i != 0:
                        case_name += '-'
                    if isinstance(param[i], np.ndarray):
                        case_name += test_info["args"][i]
                    else:
                        case_name += test_info["args"][i] + "_" + str( param[i] )
                
                test_info["case_param"][case_name] = param

                if args.level == "case":
                    collected_case_list.append(inst+'/'+test_type+'/'+case_name)
                    collected_case_num_list.append(1)
                else:
                    collected_case_num_list[-1] += 1
                
                num += 1
                if args.param_info:
                    param_dict[inst][test_type][case_name] = str(param)                
            
        else:
            if args.param_info:
                param_dict[inst][test_type] = None
            if args.level == "case":
                # if no param, just one case
                collected_case_list.append(inst+'/'+test_type)
                collected_case_num_list.append(1)
            else:
                collected_case_num_list[-1] += 1

        test_dict[test_type] = test_info
    
    return test_dict

# analyse spec file to collect tests
def analyse_spec( spec_file, args, collected_case_list, collected_case_num_list, param_dict ):

    # load information from the yml file 
    stream = open(spec_file, 'r')
    config = yaml.load(stream, Loader=yaml.SafeLoader)

    for inst, cfg in config.items(): #inst is the instruction needed to test, cfg is the env\head\template\cases\check  test configuration

        # don't handle options startswith _, which is a template for tested instruction
        if inst.startswith('_'):
            continue
        
        # take the test cases info into a dict and file to tell users
        if args.level == "inst":
            # just collect the instruction
            collected_case_list.append(inst)
            collected_case_num_list.append(0)

        if args.param_info:
            param_dict[inst] = dict()
        
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

        # get the params and check string on the basis of args.basic and args.random
        if True == args.basic:
            if 'basic_cases' in cfg:
                cases_dict = cfg['basic_cases']
                if "basic_check" in cfg:
                    check_dict = cfg['basic_check']
                elif "check" in cfg:
                    check_dict = cfg['check']
                else:
                    check_dict = dict()
            else:
                continue
        elif True == args.random:
            if 'random_cases' in cfg:
                cases_dict = cfg['random_cases']
                if "random_check" in cfg:
                    check_dict = cfg['random_check']
                elif "check" in cfg:
                    check_dict = cfg['check']                    
                else:
                    check_dict = dict()                        
            else:
                continue
        else:
            if 'cases' in cfg:
                cases_dict = cfg['cases']
                if "check" in cfg:
                    check_dict = cfg['check']
                else:
                    check_dict = dict()                        
            else:
                continue


        attrs['test'] = cases_gen( args, spec_file, inst, cases_dict, cfg['templates'], check_dict, collected_case_list, collected_case_num_list, param_dict )

        # define the test function to run tests later
        exec(f'def test_function(self, args, test_type, test_case): generate(self, args, test_type, test_case)')
        exec(f'attrs["test_function"] = test_function')

        # define a Test class to organize the test info for one inst
        globals()[f'Test_{inst}'] = type(f'Test_{inst}', (object,), attrs)


def collect_tests( args ):

    if not args.specs or len(args.specs.split()) == 0:
        # if no specs argument, default find the case from specs folder
        specs = ['specs']
    else:
        # otherwise find the case from args.specs
        specs = args.specs.split(',')

    print("collecting the tests...")

    # use this list to keep the case name and amount in different merge level(case, type, inst)
    collected_case_list = [] 
    collected_case_num_list = []

    # if need to know the detailed params from spec yaml files, use param_dict to keep that.
    param_dict = dict()

    # analyze yml file to find the test cases
    for spec in specs:
        if os.path.isdir(spec):
            spec = f'{spec}/**/*.spec.yml'
        # handle every .spec.yml file under spec folder or spec is a .spec.yml file
        for filename in glob.iglob(spec, recursive=True):

            # if dont't use --random, set random seed for each spec file to make sure params same.
            if not args.random:
                np.random.seed(args.seed)
            elif args.seed != 3428: # users can set seed for random cases for each spec file
                np.random.seed(args.seed)

            analyse_spec( filename, args, collected_case_list, collected_case_num_list, param_dict )

    os.makedirs("log", exist_ok=True)

    # log file to tell user what cases there are in the yaml files in this level
    with open("log/collected_case.log", 'w') as case_log:
        for no in range(len(collected_case_list)):
            case_log.write(collected_case_list[no])
            case_log.write(',')
            case_log.write(str(collected_case_num_list[no]))
            case_log.write('\n')


    # save cases' param into a params.yaml
    if args.param_info:
        with open("log/params.yml", 'w') as params_file:
            yaml.dump( param_dict, params_file, default_flow_style = False )

    return [collected_case_list, collected_case_num_list]
                
def get_retry_cases():
    print("retry last failed cases...")
    if os.access('log/generator_report.log', os.R_OK):
        with open('log/generator_report.log') as fp:
            cases = []
            lines = fp.read().splitlines()
            for line in lines:
                if line.startswith('PASS '):
                    continue
                cases.append(line.replace('FAIL ', ''))

            if len(cases) == 0:
                print('all pass, retry abort.')
                sys.exit(0)

            return cases
    else:
        print('could not retry without last run log.')
        sys.exit(-1)   


def get_arg_cases( arg_cases ):

    s = lambda l: l.strip()
    f = lambda l: l != '' and not l.startswith('#')
    if os.access( arg_cases, os.R_OK ):
        with open( arg_cases ) as fp:
            cases = list(filter(f, map(s, fp.read().splitlines())))
    elif arg_cases != '':
        cases = list(filter(f, map(s, arg_cases.split(','))))
    else:
        cases = []

    return cases

def select_case( collected_case_list, collected_case_num_list, cases ):

    total_case_num = 0

    if cases and len(cases) > 0:
        selected_case_list = []
        for no in range(len(collected_case_list)):
            testcase = collected_case_list[no]
            for case in cases:
                if not case in testcase:
                    continue
                selected_case_list.append(testcase)
                total_case_num += collected_case_num_list[no]
                break

        return [selected_case_list, total_case_num]                
    else:
        total_case_num = sum(collected_case_num_list)
        return [collected_case_list, total_case_num]

def progress_bar_setup( total_case_num ):

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
    task_id = progress.add_task("generation", name = "generation", total=total_case_num, start=True) 
    return [progress, task_id]    

def generator_error(case):
    with result_condition:
        result_dict[case] = "python run failed."
        result_detail_dict[case] = ''
        with open(f'build/{case}/generator.log', 'w') as f:
            f.write( result_dict[case] + '\n' + result_detail_dict[case] + '\n' )

def generator_callback(progress, task_id, completed, total):
    progress.update( task_id, completed = completed )

# call the test_function in the test class to generate the test
def generate_test( case, args ):
    # the work process need to handle the KeyboardInterrupt before the main process
    try:
        # redirect the standard output and standard error output to output, by this way, we have a clean output in command line
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
        tic.test_function( args, test_type, test_case )

        if os.path.exists(f'build/{case}'):
            os.system(f'cp -rf build/Makefile.subdir build/{case}/Makefile')

        sys.stdout = stdout
        sys.stderr = stderr

        return output
    
    except:
        if output in locals().keys():
            sys.stdout = stdout
            sys.stderr = stderr
        else:
            output = io.StringIO()

        result_dict[case] = 'python failed'

        error_output = io.StringIO()
        traceback.print_tb(sys.exc_info()[2], file=error_output)
        error_str = error_output.getvalue()
        error_str += "\nUnexpected error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1])
        result_detail_dict[case] = error_str
        with open(f'build/{case}/generator.log', 'w') as f:
            f.write( result_dict[case] + '\n' + result_detail_dict[case] + '\n' )

        # print(error_str)

        return output

def gen_report( ps, failing_info, collected_case_list, collected_case_num_list ):

    failed_num = 0
    # write the test results into log/generator_report.log
    report = open(f'log/generator_report.log', 'w')
    generator_case_log = open(f'log/generator_case.log', 'w')
    for case, p in ps:
        ok = True

        case_num = collected_case_num_list[ collected_case_list.index( case ) ]

        p_value = p.get().getvalue()
        # find case result in result_dict
        if result_dict[case] != "ok":
            reason = result_dict[case]
            ok = False    
        if p_value != '':
            with open(f'build/{case}/generator.log', 'w') as f:
                f.write( p_value )

        if not ok:
            failed_num += 1
            if failing_info:
                # use the sleep to make that the main process can get the KeyboardInterrupt from ctrl C
                time.sleep(0.5)
                print(f'FAIL {case} - {reason}')
            report.write( f'FAIL {case} - {reason}\n' )
        else:
            report.write( f'PASS {case}\n' )
            generator_case_log.write( case + ',' + str(case_num) + '\n' )
                                                                    
    report.close()
    generator_case_log.close()

    return failed_num  

def main():
    
    try:
        args = parse_argument()

        # get config information from config file, including isa options and compilation options mainly
        get_config_info(args)

        # collect test cases in spec files
        [collected_case_list, collected_case_num_list] = collect_tests( args )

        # just collect cases
        if args.collect:
            print("please look at the contents in the log/collected_case.log")
            sys.exit(0)

        if args.retry:
            cases = get_retry_cases()
        else:
            cases = get_arg_cases(args.cases) 

        os.makedirs('build', exist_ok=True)

        vmap = {
            'CC': cc, 'CFLAGS': f'{defines} {cflags}', 'LDFLAGS': '', 'OBJDUMP': objdump_cmd, 'READELF': readelf,
            'SPIKE': eval(config['spike']['cmd'].format_map({
                'path': config['spike']['path'],
                'xlen': xlen, 'vlen': vlen, 'elen': elen, 'slen': slen,
            })), 'SPIKE_OPTS': '',
            'GEM5': config['gem5']['path'], 'GEM5_OPTS': config['gem5']['options'],
            'VCS': config['vcs']['path'], 'vcstimeout':config['vcs']['vcstimeout'],
            'fsdb': config['vcs']['fsdb'], 'tsiloadmem': config['vcs']['tsiloadmem'],
            'lsf': config['lsf']['is_flag'], 'LSF_CMD': config['lsf']['cmd']

        }

        rootdir_dict = {"case": '../../../..', 'type':'../../..', 'inst': '../..'}
        vmap['ROOTDIR'] = rootdir_dict[args.level]

        os.system('cp -rf utils/make/spike.mk utils/make/*.py utils/make/Makefile build/')
        if vmap['GEM5']:
            vmap['GEM5'] = os.path.abspath(vmap['GEM5'])
            os.system('cp -rf utils/make/gem5.mk build/')
        else:
            if os.path.exists(f'build/gem5.mk'):
                os.system('rm build/gem5.mk')
        if vmap['VCS']:
            vmap['VCS'] = os.path.abspath(vmap['VCS'])
            os.system('cp -rf utils/make/vcs.mk build/')
        else:
            if os.path.exists(f'build/vcs.mk'):
                os.system('rm build/vcs.mk')

        with open('utils/make/Makefile.subdir', 'r' ) as f:
            template = f.read()
            makefile_str = template.format_map(vmap)
            with open('build/Makefile.subdir', 'w') as f_ref:
                f_ref.write(makefile_str)

        with open('utils/make/variables.mk.in', 'r') as f:
            template = f.read()
            vars = template.format_map(vmap)
            with open('build/variables.mk', 'w') as fo:
                fo.write(vars)


        with Pool(processes=args.nproc) as pool:
            
            [ selected_case_list, total_case_num ] = select_case( collected_case_list, collected_case_num_list, cases )

            [progress, task_id] = progress_bar_setup( total_case_num )

            # use generate_test to generate testcase in process pool
            ps = []
            for case in selected_case_list:
                res = pool.apply_async( generate_test, [ case, args ], 
                callback=lambda _: generator_callback( progress, task_id, tests.value, total_case_num), 
                error_callback=lambda _: generator_error(case) )
                ps.append((case, res))

            failed_num = gen_report( ps, args.failing_info, collected_case_list, collected_case_num_list )

            progress.stop()

            # print test result
            if failed_num == 0:
                print(f'{len(ps)} files generation finish, all pass.( {tests.value} tests )')
                sys.exit(0)
            else:
                if args.failing_info:
                    print(f'{len(ps)} files generation finish, {failed_num} failed.( {tests.value} tests, {fails.value} failed.)')                    
                else:
                    print(f'{len(ps)} files generation finish, {failed_num} failed.( {tests.value} tests, {fails.value} failed, please look at the log/generator_report.log for the failing information. )')

                sys.exit(-1)                        


    except KeyboardInterrupt:
        # handle the keyboardInterrupt, stop the progress bar and wait all of the processes in process  pool to stop, then exit
        if 'progress' in locals():
            progress.stop()
        if 'pool' in locals():
            pool.close()
            pool.join()
        print("Catch KeyboardInterrupt!")
        sys.exit(-1)


if __name__ == '__main__':
    main()

