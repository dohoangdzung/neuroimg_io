#! /bin/bash

TASK_ID=$1
INPUT=$2
LOG=$3

./read_write "${INPUT}" "${INPUT}_2" "${LOG}"
./read_write "${INPUT}_2" "${INPUT}_3" "${LOG}"
./read_write "${INPUT}_3" "${INPUT}_4" "${LOG}"