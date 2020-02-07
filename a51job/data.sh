#!/bin/sh
cd `dirname $0` || exit 1
/usr/bin/python3.6 ./data_analysis.py >> data.log 2>&1
