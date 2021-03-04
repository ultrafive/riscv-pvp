#!/bin/bash
pytest --template-dir=./report --template=index.html --report=output/report.html $*
