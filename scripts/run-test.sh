#!/bin/bash

script_dir=`dirname $0`

. $script_dir/env.common

rm -rf output && python run.py --nproc `nproc` "$@"
