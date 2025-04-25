#!/bin/bash
# script to clean up interfaces 

i=1
while [[ $i -le $NUM_SWITCHES ]]
do
    echo "Making s${i}"
	mkdir -p onos/app/src/main/resources/bmv2/s${i}
	$DOCKER_SCRIPTS/p4c p4c-bm2-ss --arch v1model -o "onos/app/src/main/resources/bmv2/s${i}/bmv2.json" \
		-DTARGET_BMV2 -DCPU_PORT=255 \
		--p4runtime-files "onos/app/src/main/resources/bmv2/s${i}/p4info.txt" \
		p4/s${i}/main.p4
	echo "255" > onos/app/src/main/resources/bmv2/cpu_port.txt
    (( i=i+1 ))
done

# exit 0



