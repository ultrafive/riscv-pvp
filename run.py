#!/usr/bin/env python3

from utils.simulate import simulate
from utils.params import *
from isa import *

import re
import yaml
import glob
import pytest
import os
import textwrap
import argparse
import io
import sys, inspect
from multiprocessing import Pool

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--nproc', help='run tests on n processes', type=int, default=1)
parser.add_argument('--specs', help='test specs')
parser.add_argument('--cases', help=textwrap.dedent('''\
                                    test case list string or file, for example:
                                    - Test_vsub_vv,Test_addi::test_imm_op[0-0]
                                    - cases.list'''))
parser.add_argument('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
parser.add_argument('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
parser.add_argument('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
parser.add_argument('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
parser.add_argument('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

parser.add_argument('--clang', help='path of clang compiler', default='clang')

parser.add_argument('--spike', help='path of spike simulator', default='spike')
parser.add_argument('--vcs', help='path of vcs simulator', default=None)
parser.add_argument('--fsdb', help='generate fsdb waveform file when running vcs simulator', action="store_true")
parser.add_argument('--verilator', help='path of verilator simulator', default=None)

args, pytest_args = parser.parse_known_args()
if __name__ != "__main__":
    sys.argv[1:] = pytest_args

def pytest_generate_tests(metafunc):
    # called once per each test function
    argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
    params = metafunc.cls.params[ metafunc.function.__name__ ]
    metafunc.parametrize(
        argnames, [ eval(param) if isinstance(param, str) else param for param in params ]
    )

def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f

    return decorator

if not args.specs or len(args.specs.split()) == 0:
    specs = ['specs']
else:
    specs = args.specs.split()

for spec in specs:
    if os.path.isdir(spec):
        spec = f'{spec}/**/*.spec.yml'

    for filename in glob.iglob(spec, recursive=True):
        stream = open(filename, 'r')
        config = yaml.load(stream, Loader=yaml.SafeLoader)

        for inst, cfg in config.items() :
            if inst.startswith('_'):
                continue
            #print(f'{inst}:')

            #print(cfg['templates'])
            attrs = dict()
            attrs['inst'] = globals()[inst.capitalize()]
            attrs['env'] = cfg['env']
            if 'head' in cfg:
                attrs['header'] = cfg['head']
            if 'footer' in cfg:
                attrs['footer'] = cfg['footer']
            if 'tdata' in cfg:
                attrs['tdata'] = cfg['tdata']

            attrs['argnames'] = {}
            attrs['params'] = {}
            for key, template in cfg['templates'].items():
                [name, *others] = re.split(r'\s*@\s*', key)
                if len(others) == 2:
                    _args = others[0]
                    _defaults = others[1]
                elif len(others) == 1:
                    _args = others[0]
                    _defaults = ''
                else:
                    continue

                if not name in cfg['cases'] or cfg['cases'][name] is None:
                    continue
                if _args:
                    argnames = re.split(r'\s*,\s*', _args)
                else:
                    argnames = []
                attrs['argnames'][name] = argnames
                params = cfg['cases'][name]
                attrs['params'][name] = params

                if template.strip() == '{inherit}':
                    #print(cfg['templates'])
                    template = cfg['templates'][name]

                _kw = ', '.join([f'{an}={an}' for an in argnames])

                if not 'check' in cfg or not name in cfg['check']:
                    check_str = 0
                else:
                    check_str = cfg['check'][name]

                exec(f'def {name}(self, {_args}): simulate(self, args, """{template}""", """{check_str}""", {_kw}, {_defaults})')
                exec(f'attrs[name] = {name}')
                del globals()[name]

            globals()[f'Test_{inst}'] = type(f'Test_{inst}', (object,), attrs)

def run_test(name, cases, argv):
    os.makedirs(f'build/{name}', exist_ok=True)
    output = io.StringIO()
    sys.stdout = output
    sys.stderr = output
    print(name)
    argv[0] = f'{__file__}::{cases}'
    pytest.main(['-q', '-p', 'no:warnings', f'--basetemp=build/{name}', '--alluredir=output', *argv])
    return output

def collect_tests( argv):
    stdout = sys.stdout
    stderr = sys.stderr
    output = io.StringIO()
    sys.stdout = output
    sys.stderr = output
    argv[0] = __file__
    pytest.main(['-q', '-p', 'no:warnings', f'--co', *argv])
    sys.stdout = stdout
    sys.stderr = stderr
    return output


if __name__ == "__main__":
    os.makedirs('build', exist_ok=True)
    with Pool(processes=args.nproc) as pool:
        ps = []

        out = collect_tests(sys.argv)
        fn = os.path.basename(__file__)
        specs = list(filter(lambda x: f'{fn}::' in x, out.getvalue().split('\n')))
        for spec in specs:
            spec = spec.replace(f'{fn}::', '')
            subdir = spec.replace('::', '/')
            subdir = re.sub(r'[\[\]]', '/', subdir)

            if args.cases:
                if os.access(args.cases, os.R_OK):
                    with open(args.cases) as fp:
                        cases = fp.read().splitlines()
                else:
                    cases = args.cases.split(',')

                for case in cases:
                    if not spec.startswith(case):
                        continue
                    res = pool.apply_async(run_test, [subdir, spec, sys.argv])
                    ps.append((spec, subdir, res))
            else:
                res = pool.apply_async(run_test, [subdir, spec, sys.argv])
                ps.append((spec, subdir, res))

        failed = 0

        report = open(f'build/report.log', 'w')
        for spec, n, p in ps:
            ok = True
            for line in p.get().getvalue().split('\n'):
                if line.startswith('FAILED ') or line.startswith('ERROR '):
                    print(line)
                    ok = False
            with open(f'build/{n}/test.log', 'w') as f:
                print(p.get().getvalue(), file=f)

            if not ok:
                failed += 1
                print(f'FAIL {spec}', file=report)
            else:
                print(f'PASS {spec}', file=report)
        report.close()
        if failed == 0:
            print(f'{len(ps)} tests finish, all pass.')
        else:
            print(f'{len(ps)} tests finish, {failed} failed.')
