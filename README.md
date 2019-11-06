# neuroimg_io
Investigation of file read/write operations of neuroimaging pipelines.
    
## Requirement
1. *python3*
2. *dask* 
3. *numpy*
4. *matplotlib*

## How to run
Run *plotting.py* to show the result.

# Experiment Details
## System specs
Run on Cloud VM:
- CentOS Linux release 7.6.1810 (Core)
- CPU: Intel(R) Core(TM)2 Quad CPU Q8400  @ 2.66GHz
- RAM: 15 MB of RAM, cache size = 12.9 GB
- vm.dirty_ratio = 20, vm.dirty_background_ratio = 10
- Disk: 220 GB
- Measure disk bandwidth using *dd* command (run randomly):  72.5 MBps / 346 MBps (read/write)

## Input files
There are 3 input files sized 809MB, 1619MB, 6010MB.

## How it runs

- Single task: Read input files as a binary file, increase all bytes by 1. write the output to an output file.
- Pipeline: Execute a dask.bag with sequence of 3 functions in which the output file of a task is the input of it's following task.

1. Before each single task and pipeline tasks, clear the cache with command: sudo echo 3 | sudo tee /proc/sys/vm/drop_caches
2. Run with each input file.
3. Repeat experiment for 100 times.