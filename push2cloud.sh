#! /bin/bash

echo "Copying source files to cloud..."
scp -i ~/.ssh/simgridvm-key -p ./pipeline.py centos@206.167.182.108:/mnt/io_benchmark/pipeline.py
scp -i ~/.ssh/simgridvm-key -p ./single.py centos@206.167.182.108:/mnt/io_benchmark/single.py
scp -i ~/.ssh/simgridvm-key -p ./bag.py centos@206.167.182.108:/mnt/io_benchmark/bag.py
scp -i ~/.ssh/simgridvm-key -p ./export.py centos@206.167.182.108:/mnt/io_benchmark/export.py

echo "Copying running script to cloud..."
scp -i ~/.ssh/simgridvm-key -p run.sh centos@206.167.182.108:/mnt/io_benchmark/run.sh