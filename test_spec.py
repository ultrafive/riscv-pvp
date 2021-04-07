from isa.simulate import simulate2
from tests.cases.params import workdir
from isa import *

import re
import yaml
import glob
import pytest


def pytest_generate_tests(metafunc):
    # called once per each test function
    if metafunc.function.__name__ in metafunc.cls.argnames.keys():
        argnames = metafunc.cls.argnames[ metafunc.function.__name__ ]
        params = metafunc.cls.params[ metafunc.function.__name__ ]
        metafunc.parametrize(
            argnames, [ param for param in params ]
        )

def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

for filename in glob.iglob('tests/specs/**/*.spec.yml', recursive=True):
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
            [name, _args, *others] = re.split(r'\s*@\s*', key)
            if others:
                _defaults = others[0]
            else:
                _defaults = ''
            if not name in cfg['cases']:
                continue

            if _args.strip()  != '':

                argnames = re.split(r'\s*,\s*', _args)

                attrs['argnames'][name] = argnames
                params = cfg['cases'][name]
                attrs['params'][name] = params

                _kw = ', '.join([f'{an}={an}' for an in argnames])
                exec(f'def {name}(self, {_args}): simulate2(self, """{template}""", {_kw}, {_defaults})')
            else:
                exec(f'def {name}(self): simulate2(self, """{template}""")')

            exec(f'attrs[name] = {name}')
            del globals()[name]

        globals()[f'Test_{inst}'] = type(f'Test_{inst}', (object,), attrs)