#!/bin/bash
# Deprecated code


i=1
while [[ $i -le $NUM_SWITCHES ]]
do

    # previously mapreduce-clean-app
    echo "Running mapreduce-clean-app${i}"
	docker exec -it mapreduce-bm$i bash -c \
		"cd script && ./build-spatial.sh --clean; \
		 rm -f /tmp/spatial_batch_*"

    #previously mapreduce-build-app
    echo "Running mapreduce-build-app${i}"
	docker exec -it mapreduce-bm$i bash -c \
		"cd script && \
		export MAPREDUCE_BM_MAX_PKT_SIZE=${MAX_PKT_SIZE}; \
		export MAPREDUCE_BM_MAX_BATCH_SIZE=${MAX_BATCH_SIZE}; \
		./build-spatial.sh --apps_dir /mount-dir/${DOCKER_APPS_DIR} \
			--scala_program spatial/spatial${i} --reset_cache 1"
	((i=i+1))
done
exit 0