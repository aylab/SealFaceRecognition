#! /bin/bash

python train.py -d ../photos/ -c config.py -n 10 > out_sealnet.txt 2>error_sealnet.txt&
sleep 10 # wait for splits files to be written
python train.py -d ../photos/ -c config_primnet.py -s true -n 10>out_primnet.txt 2>error_primnet.txt&
