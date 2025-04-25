# *************************************************************************
# 
#  Copyright 2025 Enkeleda Bardhi (TU Delft),
#                 Chenxing Ji (TU Delft),
#                 Ali Imran (University of Michigan),
#                 Muhammad Shahbaz (University of Michigan),
#                 Riccardo Lazzeretti (Sapienza University of Rome),
#                 Mauro Conti (University of Padua),
#                 Fernando Kuipers (TU Delft)
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# 
# *************************************************************************

export DOCKER_SCRIPTS = $(shell pwd)/../scripts
export DOCKER_APPS_DIR = mechanism
export MAX_PKT_SIZE = 1500
export MAX_BATCH_SIZE = 300
export BATCH_SIZE = 5
export RATE_PPS = 30
export FILTER_MACS =
export FILTER_TYPES = 0x800
export FILTER_IPS =
export FILTER_PROTOS = 253
export NUM_SWITCHES ?= 14 # used for experiment

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

mininet-start-experiment: interfaces-setup
	$(DOCKER_SCRIPTS)/mn-stratum.run-script python mininet/topo.py 

mininet-start-tree: interfaces-setup
	$(DOCKER_SCRIPTS)/mn-stratum.run-script python mininet/tree-topo.py 

####################################################################
# ONOS
####################################################################

onos-start:
	ONOS_APPS=gui,proxyarp,drivers.bmv2 \
	$(DOCKER_SCRIPTS)/onos

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

onos-traverse-mapreduce-sw5-path1:
	cd onos/api && python3 experiment-rules.py --num-switches 5 --path 1

onos-traverse-mapreduce-sw9-path1:
	cd onos/api && python3 experiment-rules.py --num-switches 9 --path 1


####################################################################
# P4
####################################################################

p4-build-all: p4-clean 
	${DOCKER_SCRIPTS}/p4-build-all.sh

p4-clean:
	sudo rm -rf onos/app/src/main/resources/*


####################################################################
# MapReduce
####################################################################
### Build applications
mapreduce-build-app-all: 
	${DOCKER_SCRIPTS}/mapreduce-build-app-all.sh ${NUM_SWITCHS}

mapreduce-build-app1-rc: mapreduce-clean-app1
	docker exec -it mapreduce-bm1 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial1 --reset_cache 1"

mapreduce-build-app2-rc: mapreduce-clean-app2
	docker exec -it mapreduce-bm2 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial2 --reset_cache 1"

mapreduce-build-app3-rc: mapreduce-clean-app3
	docker exec -it mapreduce-bm3 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial3 --reset_cache 1"

mapreduce-build-app4-rc: mapreduce-clean-app4
	docker exec -it mapreduce-bm4 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial4 --reset_cache 1"

mapreduce-build-app5-rc: mapreduce-clean-app5
	docker exec -it mapreduce-bm5 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial5 --reset_cache 1"

mapreduce-build-app6-rc: mapreduce-clean-app6
	docker exec -it mapreduce-bm6 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial6 --reset_cache 1"

mapreduce-build-app7-rc: mapreduce-clean-app7
	docker exec -it mapreduce-bm7 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial7 --reset_cache 1"


mapreduce-build-app8-rc: mapreduce-clean-app8
	docker exec -it mapreduce-bm8 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial8 --reset_cache 1"


mapreduce-build-app9-rc: mapreduce-clean-app9
	docker exec -it mapreduce-bm9 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial9 --reset_cache 1"

mapreduce-build-app10-rc: mapreduce-clean-app10
	docker exec -it mapreduce-bm10 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial10 --reset_cache 1"

mapreduce-build-app11-rc: mapreduce-clean-app11
	docker exec -it mapreduce-bm11 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial11 --reset_cache 1"

mapreduce-build-app12-rc: mapreduce-clean-app12
	docker exec -it mapreduce-bm12 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial12 --reset_cache 1"

mapreduce-build-app13-rc: mapreduce-clean-app13
	docker exec -it mapreduce-bm13 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial13 --reset_cache 1"

mapreduce-build-app14-rc: mapreduce-clean-app14
	docker exec -it mapreduce-bm14 bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=$(MAX_PKT_SIZE); \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=$(MAX_BATCH_SIZE); \
		./build-spatial.sh --apps_dir /mount-dir/$(DOCKER_APPS_DIR) \
			--scala_program spatial/spatial14 --reset_cache 1"



# Run applications one by one
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


mapreduce-run-app6:
	docker exec -it mapreduce-bm6 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr6 --egress-iface mr6v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"


mapreduce-run-app7:
	docker exec -it mapreduce-bm7 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr7 --egress-iface mr7v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"


mapreduce-run-app8:
	docker exec -it mapreduce-bm8 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr8 --egress-iface mr8v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app9:
	docker exec -it mapreduce-bm9 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr9 --egress-iface mr9v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"


mapreduce-run-app10:
	docker exec -it mapreduce-bm10 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr10 --egress-iface mr10v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app11:
	docker exec -it mapreduce-bm11 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr11 --egress-iface mr11v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app12:
	docker exec -it mapreduce-bm12 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr12 --egress-iface mr12v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app13:
	docker exec -it mapreduce-bm13 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr13 --egress-iface mr13v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"

mapreduce-run-app14:
	docker exec -it mapreduce-bm14 bash -c \
		"cp -f script/bm.py build/.; \
		 cd build && python3 bm.py --ingress-iface vmr14 --egress-iface mr14v \
			--batch-size $(BATCH_SIZE) --rate-pps $(RATE_PPS) --macs $(FILTER_MACS) \
			--types $(FILTER_TYPES) --ips $(FILTER_IPS) --protos $(FILTER_PROTOS)"


### Clean applications 
### Application clean now integrate inside the build script
mapreduce-clean-app1:
	docker exec -it mapreduce-bm1 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app2:
	docker exec -it mapreduce-bm2 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app3:
	docker exec -it mapreduce-bm3 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app4:
	docker exec -it mapreduce-bm4 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app5:
	docker exec -it mapreduce-bm5 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app6:
	docker exec -it mapreduce-bm6 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app7:
	docker exec -it mapreduce-bm7 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app8:
	docker exec -it mapreduce-bm8 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app9:
	docker exec -it mapreduce-bm9 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app10:
	docker exec -it mapreduce-bm10 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app11:
	docker exec -it mapreduce-bm11 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app12:
	docker exec -it mapreduce-bm12 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app13:
	docker exec -it mapreduce-bm13 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

mapreduce-clean-app14:
	docker exec -it mapreduce-bm14 bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"


####################################################################
# Hosts
####################################################################

h1:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec h1

h1-send:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec-script h1 \
        	"cd traffic && ./h1-send.sh"

h4-recv-sw5:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec-script h4 \
        	"cd traffic && ./h2-recv.sh --host h4 --num-hops 5"			
h4-recv-sw9:
	$(DOCKER_SCRIPTS)/utils/mn-stratum/exec-script h4 \
        	"cd traffic && ./h2-recv.sh --host h4 --num-hops 9"	

