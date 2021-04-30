#!/bin/bash
rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -n `nproc` --specs "$*" test_spec.py | grep -v " gw"
