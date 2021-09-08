import os

# compile the test.S
def compile(args, binary, mapfile, dumpfile, source, logfile, **kw):
    compile_config = args.compile_config

    cmd = f'{compile_config["compile_cmd"]}  -Wl,-Map,{mapfile} {source} -o {binary} >> {logfile} 2>&1'
    print(f'# {cmd}\n', file=open(logfile, 'w'))
    ret = os.system(cmd)
    if ret != 0:
        return ret

    cmd = f'{compile_config["objdump_cmd"]} {binary} 1>{dumpfile} 2>>{logfile}'
    print(f'# {cmd}\n', file=open(logfile, 'a'))    
    ret = os.system(cmd)
    if compile_config["is_objdump"]:
        return ret
    else:
        return 0