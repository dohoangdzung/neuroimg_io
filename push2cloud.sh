#! /bin/bash

echo "Copying source files to cloud..."
#scp -i ~/.ssh/simgridvm-key -p ./pipeline.py ./pipeline.py ./bag.py ./command.py ./export.py centos@206.167.182.108:/mnt/io_benchmark/export.py
scp -i ~/.ssh/simgridvm-key -p ./read.c ./read_write.c centos@206.167.182.108:/mnt/io_benchmark/read_write.c

echo "Copying running script to cloud..."
#scp -i ~/.ssh/simgridvm-key -p run.sh centos@206.167.182.108:/mnt/io_benchmark/run.sh
scp -i ~/.ssh/simgridvm-key -p run_pipeline_c.sh run_atop.sh run_readonly.sh centos@206.167.182.108:/mnt/io_benchmark/

#to cluster
scp read_write.c run_pipeline_c.sh dzung@cluster:~/io_benchmark/