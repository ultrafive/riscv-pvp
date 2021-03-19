#!/bin/bash
rm -rf output && pytest --alluredir=output --basetemp=$PWD/build $*
