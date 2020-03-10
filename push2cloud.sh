#! /bin/bash

echo "Copying source files to cloud..."
#scp -i ~/.ssh/simgridvm-key -p ./pipeline.py centos@206.167.182.108:/mnt/io_benchmark/pipeline.py
#scp -i ~/.ssh/simgridvm-key -p ./single.py centos@206.167.182.108:/mnt/io_benchmark/single.py
#scp -i ~/.ssh/simgridvm-key -p ./bag.py centos@206.167.182.108:/mnt/io_benchmark/bag.py
#scp -i ~/.ssh/simgridvm-key -p ./export.py centos@206.167.182.108:/mnt/io_benchmark/export.py
#scp -i ~/.ssh/simgridvm-key -p ./command.py centos@206.167.182.108:/mnt/io_benchmark/command.py
scp -i ~/.ssh/simgridvm-key -p ./read_write.c centos@206.167.182.108:/mnt/io_benchmark/read_write.c

echo "Copying running script to cloud..."
#scp -i ~/.ssh/simgridvm-key -p run.sh centos@206.167.182.108:/mnt/io_benchmark/run.sh
scp -i ~/.ssh/simgridvm-key -p run_c.sh centos@206.167.182.108:/mnt/io_benchmark/run_c.sh
scp -i ~/.ssh/simgridvm-key -p run_atop.sh centos@206.167.182.108:/mnt/io_benchmark/run_atop.sh
#scp -i ~/.ssh/simgridvm-key -p bench_disk.sh centos@206.167.182.108:/mnt/io_benchmark/bench_disk.sh
#scp -i ~/.ssh/simgridvm-key -p run_ruis.sh centos@206.167.182.108:/mnt/io_benchmark/run_ruis.sh