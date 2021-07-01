#!/bin/bash

script_dir=`dirname $0`

. $script_dir/env.common

python run.py --nproc `nproc` --basic-only "$@"
