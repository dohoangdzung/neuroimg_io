import matplotlib.pyplot as plt
import numpy as np

f = open('export/pipeline_mem_c.log', 'r')
lines = f.readlines()

sys_mem = []
free_mem = []
used_mem = []
# app_mem = []
cache_used = []
avai_mem = []
dirty_ratio = []
dirty_bg_ratio = []
dirty_pages = []

swap_size = []
swap_free = []

# bw_r = []
# bw_w = []
for i in range(len(lines)):
    line = lines[i]
    if line.startswith("MEM"):
        values = line.split(" ")

        sys_mem_mb = int(values[7]) * 4096 / 2 ** 20
        sys_mem.append(sys_mem_mb)

        free_mem_mb = int(values[8]) * 4096 / 2 ** 20
        free_mem.append(free_mem_mb)

        used_mem.append(sys_mem_mb - free_mem_mb)

        cache_in_mb = int(values[9]) * 4096 / 2 ** 20
        cache_used.append(cache_in_mb)
        dirty_pages.append(int(values[12]) * 4096 / 2 ** 20)

        avai_mem.append(free_mem_mb + cache_in_mb)
        dirty_ratio.append(0.2 * (free_mem_mb + cache_in_mb))
        dirty_bg_ratio.append(0.1 * (free_mem_mb + cache_in_mb))

    else:
        if line.startswith("SWP"):
            values = line.split(" ")
            swap_size.append(int(values[7]) * 4096 / 2 ** 20)
            swap_free.append(int(values[8]) * 4096 / 2 ** 20)

intervals = len(dirty_pages)
dirty_pages = np.array(dirty_pages)
time = np.arange(0, intervals)

# ==========================MEM PROFILING===================================
# memprof_file = open('export/mprofile_20191113143630.dat', 'r')
# lines = memprof_file.readlines()
# memprof_time = []
# start = float(lines[1].split(' ')[2])
# for i in range(1, len(lines)):
#     line = lines[i]
#     timestamp = float(line.split(' ')[2])
#     if timestamp - start > 0.9:
#         mem = float(line.split(' ')[1])
#         app_mem.append(mem)
#         start = timestamp
#
# for i in range(len(app_mem), intervals):
#     app_mem.append(0)


fig = plt.figure()
plt.tight_layout()

# ==========================ATOP PLOT===================================
ax1 = fig.add_subplot(2, 1, 1)
ax1.minorticks_on()
ax1.set_title("pipeline memory profiling")

# PYTHON
# start = 0.02
# read1end = 23.53
# write1start = 26.68
# write1end = 56.90
# read2start = 58.03
# read2end = 60.81
# write2start = 64.76
# write2end = 108.49
# read3start = 110.31
# read3end = 112.67
# write3start = 116.81
# write3end = 160.84

# C
start = 1578088922.567
read1end = 1578088944.653
write1start = 1578088958.261
write1end = 1578088982.909
read2start = 1578088984.643
read2end = 1578088986.824
write2start = 1578089001.055
write2end = 1578089026.693
read3start = 1578089028.978
read3end = 1578089069.075
write3start = 1578089083.655
write3end = 1578089111.399

ax1.axvspan(xmin=read1end - start, xmax=write1start - start, color="y", alpha=0.4, label="computation")
ax1.axvspan(xmin=0, xmax=read1end - start, color="g", alpha=0.2, label="task1 read")
ax1.axvspan(xmin=write1start - start, xmax=write1end - start, color="g", alpha=0.4, label="task1 write")

ax1.axvspan(xmin=read2start - start, xmax=read2end - start, color="b", alpha=0.2, label="task2 read")
ax1.axvspan(xmin=read2end - start, xmax=write2start - start, color="y", alpha=0.4)
ax1.axvspan(xmin=write2start - start, xmax=write2end - start, color="b", alpha=0.4, label="task2 write")

ax1.axvspan(xmin=read3start - start, xmax=read3end - start, color="r", alpha=0.2, label="task3 read")
ax1.axvspan(xmin=read3end - start, xmax=write3start - start, color="y", alpha=0.4)
ax1.axvspan(xmin=write3start - start, xmax=write3end - start, color="r", alpha=0.4, label="task3 write")

# app_cache = list(np.array(app_mem) + np.array(cache_used))

ax1.plot(time, sys_mem, color='k', linewidth=1.5, label="total mem")
# ax1.plot(time, free_mem, color='g', linewidth=1.5, linestyle="-.", label="free memory")
ax1.plot(time, used_mem, color='g', linewidth=1.5, label="used mem")
# ax1.plot(time, app_mem, color='c', linewidth=1.5, label="app memory")
ax1.plot(time, cache_used, color='m', linewidth=1.5, label="cache used")
# ax1.plot(time, app_cache, color='c', linewidth=1.5, label="cache + app")
ax1.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
ax1.plot(time, avai_mem, color='b', linewidth=1, linestyle="-.", label="available mem")
ax1.plot(time, dirty_ratio, color='k', linewidth=1, linestyle="-.", label="dirty_ratio")
ax1.plot(time, dirty_bg_ratio, color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio")

# plt.annotate("(1)", (10, 4000))
# plt.annotate("(2)", (40, 14000))
# plt.annotate("(3)", (62, 12000))
# plt.annotate("(4)", (70, 14000))
# plt.annotate("(5)", (104, 1700))
# plt.annotate("(6)", (104, 8600))
# plt.annotate("(7)", (115, 9500))
# plt.annotate("(8)", (115, 700))
# plt.annotate("(9)", (125, 10700))
# plt.annotate("(10)", (132, 14200))
# plt.annotate("(11)", (132, 8700))

ax1.legend(fontsize='small', loc='best')

# plot_timeframe()
# plt.title("MR=6.5GBps, MW=3.4 GBps, DR=[136,146] MBps, DW=[124,142] MBps")
# plt.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
# plt.legend()

# ==========================COLLECTL PLOT===================================
dsk_data = np.loadtxt('export/collectl-simgrid-vm-20200103.dsk.csv', skiprows=1, delimiter=',')
read = dsk_data[:, 2] / 1024
write = dsk_data[:, 6] / 1024

time = np.arange(0, len(read))

ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
ax2.minorticks_on()
ax2.set_title("disk throughput (MB)")

ax2.axvspan(xmin=read1end - start, xmax=write1start - start, color="y", alpha=0.4)
ax2.axvspan(xmin=0, xmax=read1end - start, color="g", alpha=0.2)
ax2.axvspan(xmin=write1start - start, xmax=write1end - start, color="g", alpha=0.4)

ax2.axvspan(xmin=read2start - start, xmax=read2end - start, color="b", alpha=0.2)
ax2.axvspan(xmin=read2end - start, xmax=write2start - start, color="y", alpha=0.4)
ax2.axvspan(xmin=write2start - start, xmax=write2end - start, color="b", alpha=0.4)

ax2.axvspan(xmin=read3start - start, xmax=read3end - start, color="r", alpha=0.2)
ax2.axvspan(xmin=read3end - start, xmax=write3start - start, color="y", alpha=0.4)
ax2.axvspan(xmin=write3start - start, xmax=write3end - start, color="r", alpha=0.4)

ax2.plot(time, read, color='g', linewidth=1.5, label="read")
ax2.plot(time, write, color='r', linewidth=1.5, label="write")
ax2.legend()

plt.show()
