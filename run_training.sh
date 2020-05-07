#! /usr/bin/bash

SECONDS=0
sleep 5
#python train.py -d ../photos/ -c config.py -n 5
seal_seconds= $SECONDS

SECONDS=0
sleep 8
#python train.py -d ../photos/ -c config_primnet.py -s true -n 5 
prim_seconds=$SECONDS
echo -e "sealnet running time: $seal_seconds \nprimnet running time: $prim_seconds\n"
