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

export DOCKER_SCRIPTS ?= scripts
export MOUNT_DIR ?= $(shell pwd)

####################################################################
# MapReduce
####################################################################

# start only starts one single mapreduce bm for testing purposes
mapreduce-start:
	MAPREDUCE_BM_MOUNT_DIR=$(MOUNT_DIR) \
	$(DOCKER_SCRIPTS)/mapreduce-bm

mapreduce-start-treetopo:	
	MAPREDUCE_BM_MOUNT_DIR=$(MOUNT_DIR) \
	$(DOCKER_SCRIPTS)/mapreduce-bm-n-switches 24

mapreduce-stop-treetopo:	
	docker stop mapreduce-bm1 mapreduce-bm2 mapreduce-bm3 mapreduce-bm4 mapreduce-bm5 \
		mapreduce-bm6 mapreduce-bm7 mapreduce-bm8 mapreduce-bm9 mapreduce-bm10 \
		mapreduce-bm11 mapreduce-bm12 mapreduce-bm13 mapreduce-bm14 mapreduce-bm15 \
		mapreduce-bm16 mapreduce-bm17 mapreduce-bm18 mapreduce-bm19 mapreduce-bm20 \
		mapreduce-bm21 mapreduce-bm22 mapreduce-bm23 mapreduce-bm24
