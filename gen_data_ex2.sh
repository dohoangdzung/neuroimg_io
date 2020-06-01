#! /bin/bash

rm -f /disk0/dzung/data/file*
for i in {1..32}
do
    dd if=/dev/urandom of=/disk0/dzung/data/file${i} bs=1MB count=3000
done