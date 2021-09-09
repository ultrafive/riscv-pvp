import os
import collections
import yaml
import inspect
from importlib.machinery import SourceFileLoader

from . import consts

def get_package_root():
    return os.path.dirname(os.path.realpath(__file__))

def expend_path(path):
    if path.startswith('~') or path.startswith('.'):
        return os.path.abspath(os.path.expanduser(path))
    return path

def import_from_directory(path, globals):
    if not os.path.exists(path):
        return
    for root, dirs, _ in os.walk(path):
        for d in dirs:
            for f in os.listdir(os.path.join(root, d)):
                ff = os.path.join(root, d, f)
                if not os.path.isfile(ff):
                    continue
                if not f.endswith('.py') or f == '__init__.py':
                    continue

                m = SourceFileLoader(f, ff).load_module()
                for a in dir(m):
                    attr = getattr(m, a)
                    if inspect.isclass(attr) or inspect.isfunction(attr):
                        globals[a] = attr

def parse_config_items(cfg, ctx = {}):
    for k, v in cfg.items():
        if isinstance(v, dict):
            parse_config_items(v, ctx)
            continue
        if isinstance(v, str):
            if v.startswith("f'") or v.startswith('f"'):
                cfg[k] = eval(v, ctx)
            
        ctx[k] = cfg[k]

def merge_configs(cfg, part):
    for k, v in part.items():
        if (k in cfg and isinstance(cfg[k], dict)
                and isinstance(part[k], collections.Mapping)):
            merge_configs(cfg[k], part[k])
        else:
            cfg[k] = part[k]


def parse_config_files(file):
    config = dict()
    for file in [*consts.default_configs, file]:
        with open(file, 'r') as f:
            part = yaml.load(f, Loader=yaml.SafeLoader)
            merge_configs(config, part)

    parse_config_items(config)

    return config

class Args(object):
    """Build argument object from kwargs"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)