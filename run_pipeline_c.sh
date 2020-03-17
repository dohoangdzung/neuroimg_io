#! /bin/bash

rm -f export/timestamps*.log
rm -f export/collectl-simgrid-vm*.*
rm -f export/pipeline_mem_c.log

#rm output/*.* export/pipeline_mem_c_cloud_read_only.log
#dd if=/dev/urandom of=input/file1.dat bs=2MiB count=1024
#dd if=/dev/urandom of=output/file2.dat bs=2MiB count=1024
#dd if=/dev/urandom of=output/file3.dat bs=2MiB count=1024

sudo echo 3 | sudo tee /proc/sys/vm/drop_caches

atop -P MEM 1 200 > export/pipeline_mem_c.log &
collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p  &

./read "input/6010_synthesizedFLASH25inMNI.nii.gz" "output/file2.dat" "export/timestamps_c.log"
./read "input/4702_Synthesized_FLASH25_in_MNI_v2_100um.nii.gz" "output/file3.dat"  "export/timestamps_c.log"
./read "input/1150_Synthesized_FLASH25_in_MNI_v2_200um.nii.gz" "output/file4.dat"  "export/timestamps_c.log"
./read "input/8271_Acquired_FA25_100um.nii.gz" "output/file5.dat"  "export/timestamps_c.log"
./read "input/1999_Synthesized_FLASH25_100um_TIFF_Axial_Images.zip" "output/file6.dat"  "export/timestamps_c.log"
./read "input/1024_Acquired_FA25_downsampled_200um.nii.gz" "output/file7.dat"  "export/timestamps_c.log"
