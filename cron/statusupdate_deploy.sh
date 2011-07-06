#!/usr/bin/env bash
export HOME=/home/soc1024c/
source ~/.bash_profile
pushd /home/soc1024c/statusupdate/server
./server_statusupdate.py 8180 &
popd