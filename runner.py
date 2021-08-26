#!/usr/bin/env python3

import os
import textwrap
import numpy as np
import allure
from multiprocessing import Pool, Manager, Condition, Value, Process
import sys
import io
import argparse
import time
import yaml
import re
import traceback
from utils.simulator import spike_run, sims_run
from utils.check import from_txt, diff_to_txt, check_to_txt
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
    parser.add_argument('--config', help='config yaml file, default config/prod.yml', default='config/prod.yml')
    parser.add_argument('--retry', '-r', help='retry last failed cases', action="store_true")
    parser.add_argument('--nproc', '-n', help='runner process number for run cases, default 1', type=int, default=1)
    parser.add_argument('--cases', '-c', help=textwrap.dedent('''\
                                        test case list string or file, for example:
                                        - vsub_vv,addi/test_imm_op/
                                        - cases.list'''), default='')
    parser.add_argument('--no-failing-info', '-nfi', help="don't print the failing info into the screen, but in the log/runner_report.log.", action="store_true")                                     


    # options to configure the test CPU
    # parser.add_argument('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
    # parser.add_argument('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
    # parser.add_argument('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
    # parser.add_argument('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
    # parser.add_argument('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

    # options to configure the simulator
    parser.add_argument('--lsf', help='run tests on with lsf clusters, if not set, depend on lsf:is_flag in the file set by --config', action="store_true")
    parser.add_argument('--fsdb', '-f', help='generate fsdb waveform file when running vcs simulator, if not set, depend on vcs:fsdb in the file set by --config', action="store_true")
    parser.add_argument('--tsiloadmem', '-tlm', help='Load binary through TSI instead of backdoor, if not set, depend on vcs:tsiloadmem in the file set by --config', action="store_true")
    parser.add_argument('--vcstimeout', '-vto', help='Number of cycles after which VCS stops, if not set, depend on vcs:vcstimeout in the file set by --config', default=-3333, type=int)

    args, unknown_args = parser.parse_known_args()
    if unknown_args:
        print("Please check your arguments")
        sys.exit(-1)

    return args

def sync_variable():
    # to synchronize the runner processes with the main process
    globals()["manager"] = Manager()
    globals()["result_dict"] = manager.dict()
    globals()["result_condition"] = Condition()
    globals()["result_detail_dict"] = manager.dict()
    globals()["tests"] = Value('L', 0)
    globals()["fails"] = Value('L', 0)

def get_config_info(args):

    # analyse the config yaml to get simulator info
    with open(args.config, 'r' ) as f_env:
        env = yaml.load(f_env, Loader=yaml.SafeLoader)
        args.xlen = xlen = env["processor"]['xlen']
        args.flen = flen = env["processor"]['flen']
        args.vlen = vlen = env["processor"]['vlen']
        args.elen = elen = env["processor"]['elen']
        args.slen = slen = env["processor"]['slen']

        args.lsf_cmd = lsf_cmd = env["lsf"]["cmd"]
        if args.lsf == False:
            args.is_lsf = is_lsf = env["lsf"]["is_flag"]
        else:
            args.is_lsf = True
        
        path = env["spike"]['path']
        args.spike_cmd = eval(env["spike"]['cmd'])
        
        args.gem5_path = env["gem5"]["path"]
        args.gem5_options = env["gem5"]["options"]

        args.vcs_path = env["vcs"]["path"]
        if args.vcstimeout == -3333:
            args.vcstimeout = env["vcs"]["vcstimeout"]
        if args.fsdb == False:
            args.fsdb = env["vcs"]["fsdb"]
        if args.tsiloadmem == False:
            args.tsiloadmem = env["vcs"]["tsiloadmem"]

        args.verilator_path = env["verilator"]["path"]

# run failed cases last time
def get_retry_cases():
    print("retry last failed cases...")
    if os.access('log/runner_report.log', os.R_OK):
        with open('log/runner_report.log') as fp:
            cases = []
            lines = fp.read().splitlines()
            for line in lines:
                if line.startswith('PASS '):
                    continue
                cases.append(line.replace('FAIL ', ''))
            
            return cases
            if len(cases) == 0:
                print('all pass, retry abort.')
                sys.exit(0)
    else:
        print('could not retry without last run log.')
        sys.exit(-1)

# get cases from arguments
def get_arg_cases(args_cases):
    s = lambda l: l.strip()
    f = lambda l: l != '' and not l.startswith('#')
    if os.access(args_cases, os.R_OK):
        with open(args_cases) as fp:
            cases = list(filter(f, map(s, fp.read().splitlines())))
    elif args_cases != '':
        cases = list(filter(f, map(s, args_cases.split(','))))
    else:
        cases = []   
    
    return cases

def get_generator_case():
    with open("log/generator_case.log") as fp:
        s = lambda l: l.strip()
        f = lambda l: l != '' and not l.startswith('#')
        generator_info_list = list(filter(f, map(s, fp.read().splitlines())))
        generator_case_list = []
        generator_num_list = []
        for no in range(len(generator_info_list)):
            [case_name, case_num] = re.split(r'\s*,\s*', generator_info_list[no])
            generator_case_list.append(case_name)
            generator_num_list.append(int(case_num))  

    return [generator_case_list, generator_num_list]  

def select_run_case( generator_case_list, generator_num_list, cases ):
    total_num = 0
    run_case_list = []

    if len(cases) > 0:
        for no in range(len(generator_case_list)):
            case_name = generator_case_list[no]
            for case in cases:
                if not case in case_name:
                    continue

                run_case_list.append(case_name)
                total_num += generator_num_list[no]
                break
    else:
        run_case_list = generator_case_list
        total_num = sum(generator_num_list)

    return [run_case_list, total_num]

def process_bar_setup( total_num ):
    # progress bar configurations
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
    task_id = progress.add_task("runner", name = "runner", total=total_num, start=True) 

    return [progress, task_id]

def runner_error(case):
    with result_condition:
        result_dict[case] = "python run failed."
        result_detail_dict[case] = ''

def runner_callback(progress, task_id, completed, total):
    progress.update( task_id, completed = completed )
    if completed == total and getattr( runner_callback, 'x', 0) == 0 :  
        runner_callback.x = 1
        progress.stop()
        print("analyzing the results...")

def gen_runner_report( ps, args ):
    failed_num = 0

    # save the runner result into the log file
    report = open(f'log/runner_report.log', 'w')
    for case, p in ps:
        ok = True

        p_str = p.get().getvalue()
        # find case result in result_dict
        if result_dict[case] != "ok":
            reason = result_dict[case]
            ok = False    
        with open(f'build/{case}/runner.log', 'w') as f:
            print(result_dict[case], file=f) 
            print(result_detail_dict[case], file=f)
            print(p_str, file=f)                         

        if not ok:
            failed_num += 1
            if not args.no_failing_info:                    
                time.sleep(0.5)
                print(f'FAIL {case} - {reason}')                    
            print(f'FAIL {case} - {reason}', file=report)
        else:
            print(f'PASS {case}', file=report)                                                      

    report.close()

    return failed_num    

# the main entrance of the runner process, including run in simulators and check the data
def run_test(case, args):
    try:
        stdout = sys.stdout
        stderr = sys.stderr
        output = io.StringIO()
        sys.stdout = output
        sys.stderr = output

        # file information
        binary = f'build/{case}/test.elf'
        run_mem = f'build/{case}/run.mem'
        run_log = f'build/{case}/spike.log'
        res_file = f'build/{case}/spike.sig' 
        check_golden = f'build/{case}/check_golden.npy'                   

        # get the cases list in the case, including test_num, name, check string, golden
        case_list = np.load( check_golden, allow_pickle=True )


        # run elf in spike to check if the elf is right
        ret = spike_run(args, run_mem, binary, run_log, res_file)
        if ret != 0:
            # if failed, set the result of every case as spike-run, means failed when run in spike
            # then return, stop testing this case
            with result_condition:           
                result_dict[case] = "spike-run"
                result_detail_dict[case] = f'\nspike-run failed!!!\nPlease check the spike log in {run_log} '
                fails.value += len(case_list)
                tests.value += len(case_list)

                sys.stdout = stdout
                sys.stderr = stderr

            return output   
        
        # use these two variables to keep test info for this case
        test_result = ''
        test_detail = ''

        # use this to count failed subcases in this case
        failed_case_list = []


        # check the golden result computed by python with the spike result
        spike_result = {}
        spike_start = 0
        for test_case in case_list:
            if test_case["check_str"] != '':

                # when test["check_str"] == 0, no need to check
                golden = test_case["golden"]

                #because many subcases in one signature file, so we need the spike_start to know where to find the result
                [ result, spike_start ] = from_txt( res_file, golden,  spike_start )

                #save the python golden result and spike result into check.data file of each case        
                os.makedirs(f'build/{test_case["name"]}', exist_ok=True)
                check_result = check_to_txt( golden, result, f'build/{test_case["name"]}/check.data', test_case["check_str"] )

                if not check_result:
                    # if check failed, set result as "check failed", because the elf can be run in more sims, so don't use result_dict and notify result_condition
                    test_result += test_case["name"]+"_check failed-"
                    test_detail += f'The python golden data and spike results of test case {test_case["no"]} in build/{case}/test.S check failed. You can find the data in build/{test_case["name"]}/check.data\n'
                    failed_case_list.append(test_case["name"])

                spike_result[test_case["name"]] = result



        # run case in more simulators and compare simulator results with spike results, which need to be same
        sims_result = sims_run( args, f'build/{case}', binary )
        for sim in [ "vcs", "verilator", "gem5" ]:
            if eval(f'args.{sim}_path') == None:
                # don't set the path of sim, so dont't run it and needn't judge the result
                continue

            if sims_result[sim] != 0:
                # sim run failed                       
                # because the elf maybe can be run in more sims, so don't use result_dict and notify result_condition                                                            
                test_result += sim + "_failed-"
                test_detail += f'{binary} runned unsuccessfully in {sim}, please check build/{case}/{sim}.log\n'
                failed_case_list = case_list

            else:
                # sim run successfully, so we compare the sim results with spike results
                sim_start = 0                 
                for test_case in case_list:
                    if test_case["check_str"] != '':

                        golden = test_case["golden"]
                        # get sim result, because many cases in one signature file, so we need the start to know where to find the result
                        [ result, sim_start ] = from_txt( f'build/{case}/{sim}.sig', golden,  sim_start )

                        # save the spike result and sim result into diff-sim.data
                        os.makedirs(f'build/{test_case["name"]}', exist_ok=True)  
                        diff_result = diff_to_txt( spike_result[test_case["name"]], result, f'build/{test_case["name"]}/diff-{sim}.data', "spike", sim )

                        if not diff_result:
                            # if spike result don't equal with sim result, diff failed, write 'sim_diff failed' to test_result
                            test_result += test_case["name"] + '_' + sim + "_diff failed-"
                            test_detail_dict = f'The results of spike and {sim} of test case {test_case["no"]}in build/{case}/test.S check failed. You can find the data in build/{test_case["name"]}/diff-{sim}.data\n'
                            # maybe check failed or other sim failed either so we have this judge                             
                            if test_case["name"] not in failed_case_list:
                                failed_case_list.append(test_case["name"])

        with result_condition:
            if test_result == '':            
                result_dict[case] = "ok"
                result_detail_dict[case] = ''
                tests.value += len(case_list)
            else:
                result_dict[case] = test_result
                result_detail_dict[case] = test_detail
                fails.value += len(failed_case_list)
                tests.value += len(case_list)
    

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
        print(error_str)

        return output

def main():

    try:

        args = parse_argument()

        # define some global sync variables to synchronize the runner processes with the main process
        sync_variable()

        # get config information from config file, including spike\gem5\vcs\verilator config info
        get_config_info(args)

        if args.retry:
            cases = get_retry_cases()
        else:
            cases = get_arg_cases(args.cases)
        
        print("looking for the cases...")

        [generator_case_list, generator_num_list] = get_generator_case()

        [run_case_list, total_num] = select_run_case( generator_case_list, generator_num_list, cases )

        [progress, task_id] = process_bar_setup( total_num )

        ps = []
        with Pool(processes=args.nproc) as pool:

            for case in run_case_list:
                res = pool.apply_async(run_test, [ case, args ], 
                callback=lambda _: runner_callback( progress, task_id, tests.value, total_num ), 
                error_callback=lambda _: runner_error(case)  )
                ps.append((case, res))              

              
            failed_num = gen_runner_report( ps, args )

            # spike may make that user can't input in command line, use stty echo to fix that.
            os.system("stty echo")

            if failed_num == 0:
                print(f'{len(ps)} files running finish, all pass.( {tests.value} tests )')
                sys.exit(0)
            else:
                if args.no_failing_info:
                    print(f'{len(ps)} files running finish, {failed_num} failed.( {tests.value} tests, {fails.value} failed, please look at the log/runner_report.log for the failing information. )')
                else:
                    print(f'{len(ps)} files running finish, {failed_num} failed.( {tests.value} tests, {fails.value} failed.)')               
                sys.exit(-1)
    
    except KeyboardInterrupt:
        
        if 'pool' in locals():
            pool.close()
            pool.join()
        
        if 'progress' in locals():
            progress.stop()
        
        print("Catch KeyboardInterrupt!")
        os.system("stty echo")
        sys.exit(-1)

        

    



if __name__ == "__main__":
    main()