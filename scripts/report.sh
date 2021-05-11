#!/bin/bash
allure generate --clean -o report output
cd report && python -m http.server $1
