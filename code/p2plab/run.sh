#!/bin/bash

CURRENT_WD=`pwd`
export PYTHONPATH=$PYTHONPATH:$CURRENT_WD/entangled:$CURRENT_WD/qtreactor
cd ngidht
python main.py
cd $CURRENT_WD

