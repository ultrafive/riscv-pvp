#!/bin/bash
script_dir=`dirname $0`

. $script_dir/env.common

procs=`nproc`
[ $procs -lt 24 ] || procs=24
rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -n $procs $* run.py | grep -v " gw"
