#!/bin/bash
# NUM_SWITCHES COME FROM EXPROT IN MAKEFILE

i=1
while [[ $i -le $NUM_SWITCHES ]]
do
    sudo ip link add s${i}v type veth peer name vmr${i}
    sudo ip link set s${i}v up
    sudo ip link set vmr${i} up
    sudo ip link add vs${i} type veth peer mr${i}v
    sudo ip link set vs${i} up
    sudo ip link set mr${i}v up
    echo "Setting up interfaces for s${i} complete"
    (((i++)))

done
exit 0


# sudo ip link delete s1v
# sudo ip link delete vs1