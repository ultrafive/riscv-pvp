import os

# compile the test.S
def compile(args, binary, mapfile, dumpfile, source, logfile, **kw):
    config = args.config['compile']
    pkgroot = args.pkgroot

    cc = config['cc']
    defines = config['defines']
    cflags = config['cflags']
    linkflags = config['linkflags']

    cflags += f" -I{pkgroot}/env/p -I{pkgroot}/macros/scalar -I{pkgroot}/macros/vector"
    linkflags += f" -T{pkgroot}/env/p/link.ld"

    cmd = f'{cc} {defines} {cflags} {linkflags} -Wl,-Map,{mapfile} {source} -o {binary} >> {logfile} 2>&1'
    print(f'# {cmd}\n', file=open(logfile, 'w'))
    ret = os.system(cmd)
    if ret != 0:
        return ret

    objdump = config["objdump"]
    cmd = f'{objdump} {binary} 1>{dumpfile} 2>>{logfile}'
    print(f'# {cmd}\n', file=open(logfile, 'a'))    
    ret = os.system(cmd)
    if config["is_objdump"]:
        return ret
    else:
        return 0