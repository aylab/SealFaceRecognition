#! /bin/bash

python train.py -d ../photos/ -c config.py -n 10 > seal_out.txt 2>seal_error.txt&
sleep 15 # wait for splits files to be written
python train.py -d ../photos/ -c config_primnet.py -s true -n 10 > prim_out.txt 2>prim_error.txt&
