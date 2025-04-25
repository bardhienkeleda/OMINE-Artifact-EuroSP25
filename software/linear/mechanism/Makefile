# *************************************************************************
#
# Copyright 2025 Enkeleda Bardhi (TU Delft),
#                Chenxing Ji (TU Delft),
#                Ali Imran (University of Michigan),
#                Muhammad Shahbaz (University of Michigan),
#                Riccardo Lazzeretti (Sapienza University of Rome),
#                Mauro Conti (University of Padua),
#                Fernando Kuipers (TU Delft)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# *************************************************************************

export DOCKER_SCRIPTS = $(shell pwd)/../scripts
export DOCKER_APPS_DIR = mechanism
export MAX_PKT_SIZE = 1500
export MAX_BATCH_SIZE = 100
export BATCH_SIZE = 10
export RATE_PPS = 30
export FILTER_MACS =
export FILTER_TYPES = 0x800
export FILTER_IPS =
export FILTER_PROTOS = 253
export NUM_SWITCHES ?= 5 

all: mininet-start

clean: onos-clean-app p4-clean mapreduce-clean-app tensorflow-clean


####################################################################
# Mininet
####################################################################

#

interfaces-setup:
	${DOCKER_SCRIPTS}/interfaces-setup.sh ${NUM_SWITCHS}


interfaces-clean:
	${DOCKER_SCRIPTS}/interfaces-clean.sh ${NUM_SWITCHS}

mininet-start-linear: interfaces-setup
	$(DOCKER_SCRIPTS)/mn-stratum.run-script python mininet/topo.py \
		--num-switches 5 


####################################################################
# ONOS
####################################################################

onos-start:
	ONOS_APPS=gui,proxyarp,drivers.bmv2 \
	$(DOCKER_SCRIPTS)/onos

# The **password** is: rocks
# Press CTRL+D to exit the CLI

# To test loading of output
onos-test-netcfg:
	$(DOCKER_SCRIPTS)/onos-netcfg netcfg-test.json

onos-cli:
	$(DOCKER_SCRIPTS)/onos-cli

onos-netcfg:
	$(DOCKER_SCRIPTS)/onos-netcfg netcfg.json

onos-build-app:
	cd onos/app && $(DOCKER_SCRIPTS)/maven clean package


onos-reload-app:
	$(DOCKER_SCRIPTS)/onos-app reinstall! onos/app/target/forward-1.0-SNAPSHOT.oar

onos-clean-app:
	sudo rm -rf onos/app/target

onos-bypass-mapreduce:
	cd onos/api && python3 rules.py --bypass

onos-traverse-mapreduce:
	cd onos/api && python3 rules.py --enable

onos-reset-rules:
	cd onos/api && python3 rules.py --disable

onos-test-mirroring:
	cd onos/api && python3 mirroring_rule.py

####################################################################
# P4
####################################################################

p4-build-all: p4-clean 
	${DOCKER_SCRIPTS}/p4-build-all.sh

p4-clean:
	sudo rm -rf onos/app/src/main/resources/*

p4-test-compile: p4-clean
	echo "Testing p4 compilation"
	mkdir -p onos/app/src/main/resources/bmv2/test
	${DOCKER_SCRIPTS}/p4c p4c-bm2-ss --arch v1model -o onos/app/src/main/resources/bmv2/test/bmv2.json \
		-DTARGET_BMV2 -DCPU_PORT=255 \
		--p4runtime-files onos/app/src/main/resources/bmv2/test/p4info.txt \
		p4/test/main.p4
	echo "255" > onos/app/src/main/resources/bmv2/cpu_port.txt
# ${DOCKER_SCRIPTS}/p4c p4c-bm2-ss --version


####################################################################
# Spatial Code Preparation 
####################################################################
spatial-build-all: 
	${DOCKER_SCRIPTS}/spatial-build-all.sh


####################################################################
# MapReduce
####################################################################
### Build all applications at once

mapreduce-build-app-all: 
	${DOCKER_SCRIPTS}/mapreduce-build-app-all.sh ${NUM_SWITCHS}

### Build applications one by one

mapreduce-build-app1-rc:
	docker exec -it mapreduce-bm1 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial1 --reset_cache 1"

mapreduce-build-app2-rc:
	docker exec -it mapreduce-bm2 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial2 --reset_cache 1"

mapreduce-build-app3-rc:
	docker exec -it mapreduce-bm3 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial3 --reset_cache 1"

mapreduce-build-app4-rc:
	docker exec -it mapreduce-bm4 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial4 --reset_cache 1"

mapreduce-build-app5-rc:
	docker exec -it mapreduce-bm5 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial5 --reset_cache 1"


## Run applications one by one
mapreduce-run-app1:
	docker exec -it mapreduce-bm1 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr1 --egress-iface mr1v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app2:
	docker exec -it mapreduce-bm2 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr2 --egress-iface mr2v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app3:
	docker exec -it mapreduce-bm3 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr3 --egress-iface mr3v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app4:
	docker exec -it mapreduce-bm4 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr4 --egress-iface mr4v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app5:
	docker exec -it mapreduce-bm5 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr5 --egress-iface mr5v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

### Clean applications 
### Application clean now integrate inside the build script
mapreduce-clean-app:
	docker exec -it mapreduce-bm bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

####################################################################
# Hosts
####################################################################

h1:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec h1

h2:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec h2

h1-send:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec-script h1 \
        	"cd traffic && ./h1-send.sh"

h2-recv:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec-script h2 \
        	"cd traffic && ./h2-recv.sh"
