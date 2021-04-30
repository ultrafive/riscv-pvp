from isa.simulate import simulate2
from tests.cases.params import *
from isa import *

import re
import yaml
import glob
import pytest
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--specs', help='test specs')
args, pytest_args = parser.parse_known_args()
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
    specs = ['tests/specs']
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
            print(f'{inst}:')

            print(cfg['templates'])
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
                    print(cfg['templates'])
                    template = cfg['templates'][name]

                _kw = ', '.join([f'{an}={an}' for an in argnames])

                if not 'diff' in cfg or not name in cfg['diff']:
                    diff_str = 0
                else:
                    diff_str = cfg['diff'][name]

                exec(f'def {name}(self, {_args}): simulate2(self, """{template}""", """{diff_str}""", {_kw}, {_defaults})')
                exec(f'attrs[name] = {name}')
                del globals()[name]

            globals()[f'Test_{inst}'] = type(f'Test_{inst}', (object,), attrs)
