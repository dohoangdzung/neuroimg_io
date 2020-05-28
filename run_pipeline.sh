#! /bin/bash

rm -f export/*.*
rm -f /disk0/dzung/input/*.*
rm -f /disk0/dzung/output/*.*

#dd if=/dev/urandom of=input/file1.dat bs=2MB count=20000

echo 3 | sudo tee /proc/sys/vm/drop_caches

collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p &
sleep 1
atop -P MEM 1 500 > export/pipeline_mem_c.log &

./pipeline.sh 1 "data/file1" "export/timestamps_pipeline1.csv" &
./pipeline.sh 2 "data/file2" "export/timestamps_pipeline2.csv" &
./pipeline.sh 3 "data/file3" "export/timestamps_pipeline3.csv" &
./pipeline.sh 4 "data/file4" "export/timestamps_pipeline4.csv" &

wait

