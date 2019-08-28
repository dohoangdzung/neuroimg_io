#! /bin/bash

echo "Starting running benchmark..."

INPUTS0="input/sub16.zip"
INPUTS1="input/synthesizedFLASH25inMNI_6010.nii.gz"
INPUTS2="input/synthesized_FLASH25.nii.gz"

for ((i=1;i<100;i+=1))
do
    echo "Iteration:" ${i}
    for input in ${INPUTS0} ${INPUTS1} ${INPUTS2}
    do
        echo "Single task input:" ${input}
        sudo echo 3 | sudo tee /proc/sys/vm/drop_caches
        python3 single.py ${input} ${i}
    done

    for input in ${INPUTS0} ${INPUTS1} ${INPUTS2}
    do
        echo "Bag input:" ${input}
        sudo echo 3 | sudo tee /proc/sys/vm/drop_caches
        python3 bag.py ${input} ${i}
    done

done