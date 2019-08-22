# neuroimg_io
Investigation of file read/write operations of neuroimaging pipelines
    
## Requirement
1. *python3*
2. *dask* 
3. *matplotlib*

## How to run
Run *plotting.py* to show the result.

## System specs
1. CPU: Intel(R) Core(TM)2 Quad CPU Q8400  @ 2.66GHz
2. RAM: 15 MB of RAM
3. Disk: 220 GB
4. Measure disk bandwidth using *dd* command (run randomly):  163 MBps / 696 MBps (read/write)
 
## Cases
Task detail: read input file and generate 1 output file, 1 temp file.

1. Run single task.
2. Run single task with 30s sleep time between reading and writing.
3. Execute a dask.bag with 3 mapping functions in which the output file of a task is the input of it's following task. There is no sleeping time in each task.
4. Same as case 3 but the is 30s sleep time in each task.