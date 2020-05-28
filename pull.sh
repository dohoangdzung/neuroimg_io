#! /bin/bash

#scp -i ~/.ssh/simgridvm-key -p centos@206.167.182.108:/mnt/io_benchmark/export/single.py.json export/
#scp -i ~/.ssh/simgridvm-key -p centos@206.167.182.108:/mnt/io_benchmark/export/bag.py.json export/
#scp -i ~/.ssh/simgridvm-key -p centos@206.167.182.108:/mnt/io_benchmark/export/pipeline*.log export/
#scp -i ~/.ssh/simgridvm-key -p centos@206.167.182.108:/mnt/io_benchmark/export/collectl-simgrid-vm-*.dsk export/
#scp -i ~/.ssh/simgridvm-key -p centos@206.167.182.108:/mnt/io_benchmark/export/timestamp*.log export/

#cluster
scp dzung@cluster:~/io_benchmark/export/atop_mem.log export/cluster/exp2/
scp dzung@cluster:~/io_benchmark/export/timestamps_pipeline.csv export/cluster/exp2/
scp dzung@cluster:~/io_benchmark/export/*dsk.gz export/cluster/exp2/