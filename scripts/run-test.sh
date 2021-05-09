#!/bin/bash

script_dir=`dirname $0`

. $script_dir/env.common

rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -v $* run.py
