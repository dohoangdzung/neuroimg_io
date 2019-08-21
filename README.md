# neuroimg_io
Investigation of read/write operations of neuroimaging data files
    
## Requirement
1. python3
2. dask 
3. matplotlib

## How to run
Run *plotting.py* to show the result.


## System specs
1. CPU: Intel(R) Core(TM)2 Quad CPU Q8400  @ 2.66GHz
2. RAM: 15 MB of RAM
3. Disk: 220 GB
 
## Cases
Task detail: read input file and generate 2 output files.

1. Run single task.
2. Run single task with 30s sleep time between reading and writing.
3. Execute a dask.bag with 3 mapping functions in which the output file of a task is the input of it's following task. There is no sleeping time in each task.
4. Same as case 3 but the is 30s sleep time in each task.