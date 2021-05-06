#!/bin/bash
. env.common

rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -v $* test_spec.py
