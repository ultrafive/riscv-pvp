#!/bin/bash
rm -rf output && pytest --alluredir=output --basetemp=$PWD/build -v --specs "$*" test_spec.py
