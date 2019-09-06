# neuroimg_io
Investigation of file read/write operations of neuroimaging pipelines
    
## Requirement
1. *python3*
2. *dask* 
3. *numpy*
4. *matplotlib*

## How to run
Run *plotting.py* to show the result.

## System specs
1. CPU: Intel(R) Core(TM)2 Quad CPU Q8400  @ 2.66GHz
2. RAM: 15 MB of RAM
3. vm.dirty_ratio = 20, vm.dirty_background_ratio = 10
4. Disk: 220 GB
5. Measure disk bandwidth using *dd* command (run randomly):  72.5 MBps / 346 MBps (read/write)
 
## Cases
Task detail: read input file, increase every byte of input file by 1, and generate 1 output file.

1. Run single task with different input files.
2. Execute a dask.bag with 3 mapping functions in which the output file of a task is the input of it's following task.