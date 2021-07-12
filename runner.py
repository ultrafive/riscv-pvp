#!/usr/bin/env python3

import os
import textwrap
import numpy as np
import allure
from multiprocessing import Pool, Manager, Condition, Value
import sys
import io
import argparse
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
# options to configure the test frame
parser.add_argument('--retry', help='retry last failed cases', action="store_true")
parser.add_argument('--runner_process', help='runner process number for run cases', type=int, default=1)
parser.add_argument('--cases', help=textwrap.dedent('''\
                                    test case list string or file, for example:
                                    - vsub_vv,addi/test_imm_op/
                                    - cases.list
                                    default = log/runner_case.log'''), default='log/runner_case.log')

# options to configure the test CPU
parser.add_argument('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
parser.add_argument('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
parser.add_argument('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
parser.add_argument('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
parser.add_argument('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

# options to configure the simulator
parser.add_argument('--lsf', help='run tests on with lsf clusters', action="store_true")                                    
parser.add_argument('--spike', help='path of spike simulator', default='spike')
parser.add_argument('--vcs', help='path of vcs simulator', default=None)
parser.add_argument('--gem5', help='path of gem5 simulator', default=None)
parser.add_argument('--fsdb', help='generate fsdb waveform file when running vcs simulator', action="store_true")
parser.add_argument('--tsiloadmem', help='Load binary through TSI instead of backdoor', action="store_true")
parser.add_argument('--vcstimeout', help='Number of cycles after which VCS stops', default=1000000, type=int)
parser.add_argument('--verilator', help='path of verilator simulator', default=None)

args, unknown_args = parser.parse_known_args()


# to synchronize the runner processes with the main process
manager = Manager()
result_dict = manager.dict()
result_condition = Condition()
result_detail_dict = manager.dict()
tests = Value('L', 0)
fails = Value('L', 0)

# run test.elf in spike
def spike_run(args, memfile, binary, logfile, res_file, **kw):
    sim = f'{args.spike} --isa=rv{args.xlen}gcv_zfh --varch=vlen:{args.vlen},elen:{args.elen},slen:{args.slen}'

    cmd = f'{sim} +signature={res_file} +signature-granularity={32} {binary} >> {logfile} 2>&1'
    print(f'# {cmd}\n', file=open(logfile, 'w'))
    ret = os.system(cmd)
    return ret

# find the result from the start location of signature file 
def from_txt(fpath, golden, start ):
    ebyte = golden.itemsize
    size = golden.size
    dtype = golden.dtype
    # we need to save the result align ebyte so we need align_size here
    align_size = ebyte

    if golden.dtype == np.bool_:
        # set ebyte to 0.1 to be different with e8
        ebyte = 0.1
        align_size = 1

    result = []
    now = 0
    # we recompute the start location in order to satisfy the align mechanism
    if start % align_size != 0:
        start = ( start // align_size + 1 ) * align_size
    with open(fpath) as file:
        for line in file:
            line = line.rstrip()
            if start - now >= 32:
                # if start bigger than this line, continue to next line
                now += 32
                continue
            else:  
                # if start is in this line, we use start-now as line_start
                # if not we use 0 as line_start                
                line_start = start - now
                if line_start < 0:
                    line_start = 0    

                if ebyte != 0.1:
                    # handle e8\e16\e32\e64
                    while line_start != 32:
                        # we get hex string from end to start because they are saved in that way
                        if line_start == 0:
                            str = line[-2*ebyte:]
                        else:
                            str = line[-2*(ebyte+line_start): -2*line_start]
                        
                        line_start += ebyte
                        num = int( str, 16 )
                        result.append( num )                    

                else:
                    # handle mask register
                    # every hex char have 4 bits
                    for no in range(2*line_start, 64):
                        str = line[ 63-no ]
                        num = int(str, 16)
                        result.append( num >> 0 & 1 )
                        result.append( num >> 1 & 1 )
                        result.append( num >> 2 & 1 )
                        result.append( num >> 3 & 1 )
                
                now += 32
                if len(result) >= size:
                    # if we get enough result, break the loop
                    break

    # get size of element in result as final result
    result = result[:size]
    
    # update start
    if ebyte == 0.1:
        ebyte = 1
        # start's unit is byte and bits save in byte, so start plus enough bytes
        if size % 8 != 0:
            start += size // 8 + 1
        else:
            start += size / 8
    else:
        # start plus size of the ebyte
        start += size * ebyte 
         
    # make data into a np.ndarray and same dtype and shape with golden
    data = np.array(result, dtype='uint%d' % (ebyte*8))
    data.dtype = dtype
    data = data.reshape( golden.shape )

    return [data, start]

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

# run test.elf in more simulator: gem5 vcs ...
def sims_run( args, workdir, binary ):
    lsf_cmd = 'bsub -n 1 -J simv -Ip'    
    sims = { 'vcs': args.vcs, 'verilator': args.verilator, 'gem5': args.gem5 }
    options = ''
    result = { 'vcs': 0, 'verilator': 0, 'gem5': 0 }
    for k, sim in sims.items():
        if sim == None:
            # don't set the path of sim, so don't run it
            continue

        # set options of sim
        if k != 'gem5':
            options = f'+signature={workdir}/{k}.sig +signature-granularity={32}'
        if k == 'vcs':            
            ret = os.system(f'smartelf2hex.sh {binary} > {workdir}/test.hex')
            if ret != 0:
                result[k] = ret
                continue

            opt_ldmem = f'+loadmem={workdir}/test.hex +loadmem_addr=80000000 +max-cycles={args.vcstimeout}'
            if args.tsiloadmem:
                opt_ldmem = f'+max-cycles={args.vcstimeout}'
            opt_fsdb = ''
            if args.fsdb:
                opt_fsdb = f'+fsdbfile={workdir}/test.fsdb'
            options += f' +permissive {opt_fsdb} {opt_ldmem} +permissive-off'
        elif k == 'gem5':
            config_file = '/'
            config_file = config_file.join(sim.split('/')[:-3]) + '/configs/example/fs.py'
            options += f'--debug-flags=Fetch,Exec \
                        {config_file} \
                        --cpu-type=MinorCPU \
                        --bp-type=LTAGE \
                        --num-cpu=1 \
                        --mem-channels=1 \
                        --mem-size=3072MB \
                        --caches \
                        --l1d_size=32kB \
                        --l1i_size=32kB \
                        --cacheline_size=64 \
                        --l1i_assoc=8 \
                        --l1d_assoc=8 \
                        --l2cache \
                        --l2_size=512kB \
                        --signature={workdir}{k}.sig'

        # set the cmd to run the sim and save the cmd
        if k == 'gem5':
            cmd = f'{sim} {options} --kernel={binary} >> {workdir}/{k}.log 2>&1'
        else:
            cmd = f'{sim} {options} {binary} >> {workdir}/{k}.log 2>&1'
        print(f'# {cmd}\n', file=open(f'{workdir}/{k}.log', 'w'))

        if args.lsf:
            cmd = f'{lsf_cmd} {cmd}'

        # run the cmd and save the result
        ret = os.system(cmd)
        result[k] = ret

    return result

# the main entrance of the runner process, including run in simulators and check the data
def runner(test):
    stdout = sys.stdout
    stderr = sys.stderr
    output = io.StringIO()
    sys.stdout = output
    sys.stderr = output

    # file information
    binary = f'build/{test}/test.elf'
    run_mem = f'build/{test}/run.mem'
    run_log = f'build/{test}/spike.log'
    res_file = f'build/{test}/spike.sig' 
    check_golden = f'build/{test}/check_golden.npy'                   

    # get the golden
    case_list = np.load( check_golden, allow_pickle=True )

    #run the elf compiled
    ret = spike_run(args, run_mem, binary, run_log, res_file)
    if ret != 0:
        # if failed, set the result of every case as spike-run, means failed when run in spike
        with result_condition:           
            result_dict[test] = "spike-run"
            result_detail_dict[test] = f'\nspike-run failed!!!\nPlease check the spike log in {run_log} '
            fails.value += len(case_list)
            tests.value += len(case_list)

            sys.stdout = stdout
            sys.stderr = stderr

        return output            

    # check the golden result computed by python with the spike result
    spike_result = {}
    spike_start = 0

    
    test_result = ''
    test_detail = ''

    failed_case_list = []
    for test_case in case_list:
        if test_case["check_str"] != '':
            # when test["check_str"] == 0, no need to check
            golden = test_case["golden"]
            #because many cases in one signature file, so we need the spike_start to know where to find the result
            [ result, spike_start ] = from_txt( res_file, golden,  spike_start )
            #save the python golden result and spike result into check.data file of each case         
            os.makedirs(f'build/{test_case["name"]}', exist_ok=True)            
            diff_to_txt( golden, result, f'build/{test_case["name"]}/check.data' )
            if not eval(test_case["check_str"]):
                # if check failed, set result as "check failed", because the elf can be run in more sims, so don't use result_dict and notify result_condition
                test_result += test_case["name"]+"_check failed-"
                test_detail += f'The python golden data and spike results of test case {test_case["no"]} in build/{test}/test.S check failed. You can find the data in build/{test_case["name"]}/check.data\n'
                failed_case_list.append(test_case["name"])

            spike_result[test_case["name"]] = result


    sims_result = sims_run( args, f'build/{test}', binary )
    for sim in [ "vcs", "verilator", "gem5" ]:
        if eval("args."+sim) == None:
            # don't set the path of sim, so dont't run it and needn't judge the result
            continue

        if sims_result[sim] != 0:
            # sim run failed                       
            # because the elf maybe can be run in more sims, so don't use result_dict and notify result_condition                                                            
            test_result += sim + "_failed-"
            test_detail += f'{binary} runned unsuccessfully in {sim}, please check build/{test}/{sim}.log\n'
            failed_case_list = case_list

        else:
            # sim run successfully, so we compare the sim results with spike results
            sim_start = 0                 
            for test_case in case_list:
                if test_case["check_str"] != '0':
                    golden = test_case["golden"]
                    # get sim result, because many cases in one signature file, so we need the start to know where to find the result
                    [ result, sim_start ] = from_txt( f'build/{test}/{sim}.sig', golden,  sim_start )
                    # save the spike result and sim result into diff-sim.data
                    os.makedirs(f'build/{test_case["name"]}', exist_ok=True)  
                    diff_to_txt( spike_result[test_case["name"]], result, f'build/{test_case["name"]}/diff-{k}.data' )
                    if not np.array_equal( spike_result[test_case["name"]], result, equal_nan=True):
                        # if spike result don't equal with sim result, diff failed, write sim_diff to test_result
                        # maybe check failed or other sim failed either so we have this judge  
                        test_result += test_case["name"] + '_' + sim + "_diff failed-"
                        test_detail_dict = f'The results of spike and {sim} of test case {test_case["no"]}in build/{test}/test.S check failed. You can find the data in build/{test_case["name"]}/diff-{k}.data\n'                                    
                        if test_case["name"] not in failed_case_list:
                            failed_case_list.append(test_case["name"])

    with result_condition:
        if test_result == '':            
            result_dict[test] = "ok"
            result_detail_dict[test] = ''
            tests.value += len(case_list)
        else:
            result_dict[test] = test_result
            result_detail_dict[test] = test_detail
            fails.value += len(failed_case_list)
            tests.value += len(case_list)
  

    sys.stdout = stdout
    sys.stderr = stderr

    return output   
              
def runner_error(case):
    with result_condition:
        result_dict[case] = "python run failed."
        result_detail_dict[case] = ''

if __name__ == "__main__":

    if args.retry:
        print("retry last failed cases...")
        if os.access('log/runner_report.log', os.R_OK):
            with open('log/runner_report.log') as fp:
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
            print('could not find case to run, please check.')
            sys.exit(-1)

    with Pool(processes=args.runner_process) as pool:
        ps = []   

        # read the all_case.log file and find the cases about the args.case option, so we know the amount of test cases we will run
        testcase_num = 0
        with open("log/all_case.log") as fp:
            s = lambda l: l.strip()
            f = lambda l: l != '' and not l.startswith('#')
            testcase_list = list(filter(f, map(s, fp.read().splitlines())))

        for testcase in testcase_list:
            for case in cases:
                if not testcase.startswith(case):                        
                    continue

                testcase_num += 1
                break

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
        task_id = progress.add_task("runner", name = "runner", total=testcase_num, start=True)                                           
        

        for case in cases:
            res = pool.apply_async(runner, [ case ], 
            callback=lambda _: progress.update( task_id, completed = tests.value ), 
            error_callback=lambda _: runner_error(case)  )
            ps.append((case, res))   


        failed = 0
        # save the runner result into the log file
        report = open(f'log/runner_report.log', 'w')
        for case, p in ps:
            ok = True

            p_str = p.get().getvalue()
            # find case result in result_dict
            if result_dict[case] != "ok":
                reason = result_dict[case] + p_str
                ok = False    
            with open(f'build/{case}/runner.log', 'w') as f:
                print(result_dict[case], file=f) 
                print(result_detail_dict[case], file=f) 
                print(p_str, file=f)                         

            if not ok:
                failed += 1
                print(f'FAIL {case} - {reason}')
                print(f'FAIL {case} - {reason}', file=report)
            else:
                print(f'PASS {case}', file=report)                                                      



        report.close()

        progress.stop() 

        if failed == 0:
            print(f'{len(ps)} files running finish, all pass.( {tests.value} tests )')
            sys.exit(0)
        else:
            print(f'{len(ps)} files running finish, {failed} failed.( {tests.value} tests, {fails.value} failed )')
            sys.exit(-1)