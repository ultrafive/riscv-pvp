import os

# run test.elf in spike
def spike_run(args, memfile, binary, logfile, res_file, **kw):    

    cmd = f'{args.spike_cmd} +signature={res_file} +signature-granularity={32} {binary} >> {logfile} 2>&1'
    print(f'# {cmd}\n', file=open(logfile, 'w'))
    ret = os.system(cmd)
    return ret

# run test.elf in more simulator: gem5 vcs ...
def sims_run( args, workdir, binary ):   
    sims = { 'vcs': args.vcs_path, 'verilator': args.verilator_path, 'gem5': args.gem5_path }
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
            options += args.gem5_options
            options += '--signature={workdir}/{k}.sig'                        

        # set the cmd to run the sim and save the cmd
        if k == 'gem5':
            cmd = f'{sim} {options} --kernel={binary} >> {workdir}/{k}.log 2>&1'
        else:
            cmd = f'{sim} {options} {binary} >> {workdir}/{k}.log 2>&1'
        print(f'# {cmd}\n', file=open(f'{workdir}/{k}.log', 'w'))

        if args.is_lsf:
            cmd = f'{args.lsf_cmd} {cmd}'

        # run the cmd and save the result
        ret = os.system(cmd)
        result[k] = ret

    return result    