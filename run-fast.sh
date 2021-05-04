#!/bin/bash
. env.common

procs=`nproc`
[ $procs -lt 24 ] || procs=24
rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -n $procs $* test_spec.py | grep -v " gw"
