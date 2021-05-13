#!/bin/bash
script_dir=`dirname $0`

. $script_dir/env.common

allure generate --clean -o report output
cd report && python -m http.server $1
