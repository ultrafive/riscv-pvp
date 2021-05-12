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
import sys, inspect

parser = argparse.ArgumentParser()
parser.add_argument('--specs', help='test specs')
parser.add_argument('--cases', help=textwrap.dedent('test cases,\nfor example: Test_addi::test_imm_op[0-0]'))
parser.add_argument('--xlen', help='bits of int register (xreg)', default=64, choices=[32,64], type=int)
parser.add_argument('--flen', help='bits of float register (freg)', default=64, choices=[32,64], type=int)
parser.add_argument('--vlen', help='bits of vector register (vreg)', default=1024, choices=[256, 512, 1024, 2048], type=int)
parser.add_argument('--elen', help='bits of maximum size of vector element', default=64, choices=[32, 64], type=int)
parser.add_argument('--slen', help='bits of vector striping distance', default=1024, choices=[256, 512, 1024, 2048], type=int)

parser.add_argument('--clang', help='path of clang compiler', default='clang')

parser.add_argument('--spike', help='path of spike simulator', default='spike')
parser.add_argument('--vcs', help='path of vcs simulator', default=None)
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

if __name__ == "__main__":
    for name, obj in list(globals().items()):
        if not name.startswith('Test_'):
            continue
        if args.cases:
            if args.cases.startswith(name):
                print(name, end=' ')
                sys.argv[0] = f'{__file__}::{args.cases}'
                pytest.main(['-p', 'no:warnings', '--basetemp=build', '--alluredir=output', *sys.argv])
        else:
            print(name, end=' ')
            sys.argv[0] = f'{__file__}::{name}'
            pytest.main(['-p', 'no:warnings', '--basetemp=build', '--alluredir=output', *sys.argv])
