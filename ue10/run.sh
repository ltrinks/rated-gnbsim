#!/bin/bash

mkdir logs/$1
cd logs/$1

../../../gnbsimwithchanges/gnbsim --cfg ../../default.yaml 2>/dev/null | grep E2E | awk 'BEGIN { FS="," } /1/ { print $7 }' > latencies.txt
