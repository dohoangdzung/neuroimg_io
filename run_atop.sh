#! /bin/bash

sudo echo 3 | sudo tee /proc/sys/vm/drop_caches
#atop -P MEM,DSK 1 200 > export/pipeline_mem.log &
atop -P MEM,DSK,SWP 1 200 > export/pipeline_mem.log &
mprof run python3 bag.py input/synthesizedFLASH25inMNI_6010.nii
