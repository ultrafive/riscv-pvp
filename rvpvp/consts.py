import os

package_root = os.path.dirname(os.path.realpath(__file__))

default_config_dir = os.path.join(package_root, 'config')
default_configs = []
for f in os.listdir(default_config_dir):
    ff = os.path.join(default_config_dir, f)
    if os.path.isfile(ff):
        default_configs.append(ff)
