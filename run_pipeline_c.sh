#! /bin/bash

rm -f export/timestamps*.csv
rm -f export/collectl-*.*
rm -f export/pipeline_mem*.log
rm -f /disk0/dzung/output/*.*

#dd if=/dev/urandom of=input/file1.dat bs=2MB count=1000

echo 3 | sudo tee /proc/sys/vm/drop_caches

collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p  &
sleep 1
atop -P MEM 1 500 > export/pipeline_mem_c.log &

./read_write "input/file1.dat" "output/file2.dat"   "export/timestamps_pipeline.csv"
./read_write "output/file2.dat" "output/file3.dat"  "export/timestamps_pipeline.csv"
./read_write "output/file3.dat" "output/file4.dat"  "export/timestamps_pipeline.csv"
