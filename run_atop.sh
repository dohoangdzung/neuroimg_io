#! /bin/bash

sudo echo 3 | sudo tee /proc/sys/vm/drop_caches
atop -P MEM 1 200 > export/pipeline_mem.log &
mprof run --include-children bag.py input/synthesizedFLASH25inMNI_6010.nii.gz
