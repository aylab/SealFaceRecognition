#! /usr/bin/bash

a=$SECONDS
python train.py -d ../photos/ -c config.py -n 5
seal_seconds=$(( SECONDS - a ))
b=$SECONDS
python train.py -d ../photos/ -c config_primnet.py -s true -n 5 
prim_seconds=$(( SECONDS - b ))
echo 'sealnet running time: $seal_seconds \nprimnet running time: $prim_seconds\n'
