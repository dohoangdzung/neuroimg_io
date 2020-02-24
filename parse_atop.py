import matplotlib.pyplot as plt
import numpy as np
import json

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


with open('export/timestamps_c.json') as json_file:
    data = json.load(json_file)
    start = data["start"]
    read1end = data["read1end"]
    write1start = data["write1start"]
    write1end = data["write1end"]
    read2start = data["read2start"]
    read2end = data["read2end"]
    write2start = data["write2start"]
    write2end = data["write2end"]
    read3start = data["read3start"]
    read3end = data["read3end"]
    write3start = data["write3start"]
    write3end = data["write3end"]


def timestamp_plot(fig):
    fig.axvspan(xmin=read1end - start, xmax=write1start - start, color="k", alpha=0.2, label="computation")
    fig.axvspan(xmin=0, xmax=read1end - start, color="g", alpha=0.2, label="read")
    fig.axvspan(xmin=write1start - start, xmax=write1end - start, color="b", alpha=0.2, label="write")

    fig.axvspan(xmin=read2start - start, xmax=read2end - start, color="g", alpha=0.2)
    fig.axvspan(xmin=read2end - start, xmax=write2start - start, color="k", alpha=0.2)
    fig.axvspan(xmin=write2start - start, xmax=write2end - start, color="b", alpha=0.2)

    fig.axvspan(xmin=read3start - start, xmax=read3end - start, color="g", alpha=0.2)
    fig.axvspan(xmin=read3end - start, xmax=write3start - start, color="k", alpha=0.2)
    fig.axvspan(xmin=write3start - start, xmax=write3end - start, color="b", alpha=0.2)


def mem_plot(fig):
    fig.minorticks_on()
    fig.set_title("pipeline memory profiling")
    timestamp_plot(fig)

    # app_cache = list(np.array(app_mem) + np.array(cache_used))

    fig.plot(time, sys_mem, color='k', linewidth=1.5, label="total mem")
    # ax1.plot(time, free_mem, color='g', linewidth=1.5, linestyle="-.", label="free memory")
    fig.plot(time, used_mem, color='g', linewidth=1.5, label="used mem")
    # ax1.plot(time, app_mem, color='c', linewidth=1.5, label="app memory")
    fig.plot(time, cache_used, color='m', linewidth=1.5, label="cache used")
    # ax1.plot(time, app_cache, color='c', linewidth=1.5, label="cache + app")
    fig.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
    fig.plot(time, avai_mem, color='b', linewidth=1, linestyle="-.", label="available mem")
    fig.plot(time, dirty_ratio, color='k', linewidth=1, linestyle="-.", label="dirty_ratio")
    fig.plot(time, dirty_bg_ratio, color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio")

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

    fig.legend(fontsize='small', loc='best')

    # plot_timeframe()
    # plt.title("MR=6.5GBps, MW=3.4 GBps, DR=[136,146] MBps, DW=[124,142] MBps")
    # plt.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
    # plt.legend()


def collectl_plot(fig):
    dsk_data = np.loadtxt('export/collectl-simgrid-vm-20200103.dsk.csv', skiprows=1, delimiter=',')
    read = dsk_data[:, 2] / 1024
    write = dsk_data[:, 6] / 1024

    time = np.arange(0, len(read))

    fig.minorticks_on()
    fig.set_title("disk throughput (MB)")

    timestamp_plot(fig)

    fig.plot(time, read, color='g', linewidth=1.5, label="read")
    fig.plot(time, write, color='r', linewidth=1.5, label="write")
    fig.legend(fontsize='small', loc='best')


figure = plt.figure()
plt.tight_layout()
ax1 = figure.add_subplot(2, 1, 1)
ax2 = figure.add_subplot(2, 1, 2, sharex=ax1)

mem_plot(ax1)
collectl_plot(ax2)

plt.show()
