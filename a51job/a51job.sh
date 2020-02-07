#!/bin/sh
cd `dirname $0` || exit 1
/usr/bin/python3.6 ./main.py >>a51job.log 2>&1 
