#! /bin/bash

rm file2.dat file3.dat file4.dat export/pipeline_mem_c.log
sudo echo 3 | sudo tee /proc/sys/vm/drop_caches

atop -P MEM 1 200 > export/pipeline_mem_c.log &
collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p  &

./read_write "input/synthesizedFLASH25inMNI_6010.nii.gz" "file2.dat"
./read_write "file2.dat" "file3.dat"
./read_write "file3.dat" "file4.dat"
