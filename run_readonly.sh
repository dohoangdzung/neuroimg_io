#! /bin/bash

rm -f export/timestamps*.log
rm -f export/collectl-simgrid-vm*.*
rm -f export/pipeline_mem_c.log

sudo echo 3 | sudo tee /proc/sys/vm/drop_caches

atop -P MEM 1 200 > export/pipeline_mem_readonly.log &
collectl -sCDnfM -omT --dskopts z --cpuopts z -i 1 --sep , -P -f export/collectl --procfilt P p  &

./read "input/6010_synthesizedFLASH25inMNI.nii.gz" "export/timestamps_readonly.log"
./read "input/4702_Synthesized_FLASH25_in_MNI_v2_100um.nii.gz"  "export/timestamps_readonly.log"
./read "input/8271_Acquired_FA25_100um.nii.gz"  "export/timestamps_readonly.log"
./read "input/1999_Synthesized_FLASH25_100um_TIFF_Axial_Images.zip" "export/timestamps_readonly.log"
./read "input/1150_Synthesized_FLASH25_in_MNI_v2_200um.nii.gz" "export/timestamps_readonly.log"
./read "input/1150_Synthesized_FLASH25_in_MNI_v2_200um.nii" "export/timestamps_readonly.log"
./read "input/1024_Acquired_FA25_downsampled_200um.nii.gz" "export/timestamps_readonly.log"
./read "input/1024_Acquired_FA25_downsampled_200um.nii" "export/timestamps_readonly.log"
./read "input/1029_Synthesized_FLASH25_downsampled_200um.nii.gz" "export/timestamps_readonly.log"
./read "input/1029_Synthesized_FLASH25_downsampled_200um.nii" "export/timestamps_readonly.log"
