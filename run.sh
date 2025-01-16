#!/bin/sh
./init.py
python central.py &
python train.py &
python lineman.py
