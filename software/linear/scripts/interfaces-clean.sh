#!/bin/bash
# script to clean up interfaces 
# NUM_SWITCHES COME FROM EXPROT IN MAKEFILE

i=1
while [[ $i -le $NUM_SWITCHES ]]
do
    sudo ip link delete s${i}v
    sudo ip link delete vs${i}
    (((i++)))

done
exit 0