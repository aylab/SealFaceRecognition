#! /usr/bin/bash

python train.py -d ../photos/ -c config.py -n 5
sleep 60 # wait for splits files to be written
python train.py -d ../photos/ -c config_primnet.py -s true -n 5 
