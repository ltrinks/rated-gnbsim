#!/bin/bash

export TIME=$(date +"%Y_%m_%d.%H_%M_%S_%N")
export TIME=${TIME// /_}
mkdir logs/$TIME
cd logs/$TIME

../../../gnbsim/gnbsim --cfg ../../default.yaml &>/dev/null
