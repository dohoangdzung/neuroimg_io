#! /bin/bash

echo "Copying source files to cloud..."
scp -i ~/.ssh/simgridvm-key -p pipeline.py centos@206.167.182.108:/mnt/io_benchmark/
scp -i ~/.ssh/simgridvm-key -p single.py centos@206.167.182.108:/mnt/io_benchmark/
scp -i ~/.ssh/simgridvm-key -p bag.py centos@206.167.182.108:/mnt/io_benchmark/
scp -i ~/.ssh/simgridvm-key -p export.py centos@206.167.182.108:/mnt/io_benchmark/

echo "Copying running script to cloud..."
scp -i ~/.ssh/simgridvm-key -p run.sh centos@206.167.182.108:/mnt/io_benchmark/