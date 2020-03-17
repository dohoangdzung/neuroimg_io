#! /bin/bash

rm -f export/timestamps*.log
rm -f export/collectl-simgrid-vm*.*
rm -f export/pipeline_mem_c.log

#rm output/file2.dat output/file3.dat output/file4.dat export/pipeline_mem_c_cloud_read_only.log
#dd if=/dev/urandom of=input/file1.dat bs=2MiB count=1024
#dd if=/dev/urandom of=output/file2.dat bs=2MiB count=1024
#dd if=/dev/urandom of=output/file3.dat bs=2MiB count=1024

sudo echo 3 | sudo tee /proc/sys/vm/drop_caches

atop -P MEM 1 200 > export/pipeline_mem_c.log &
collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p  &

./read_write "input/file1.dat" "output/file2.dat" "export/timestamps_c_readonly.log"
./read_write "output/file2.dat" "output/file3.dat" "export/timestamps_c_readonly.log"
./read_write "output/file3.dat" "output/file4.dat" "export/timestamps_c_readonly.log"
