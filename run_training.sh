#! /usr/bin/bash

SECONDS=0
python train.py -d ../photos/ -c config.py -n 10
seal_seconds=$SECONDS

SECONDS=0
python train.py -d ../photos/ -c config_primnet.py -s true -n 10 
prim_seconds=$SECONDS
echo -e "sealnet running time: $seal_seconds s \nprimnet running time: $prim_seconds s\n"
