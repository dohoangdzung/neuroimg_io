import matplotlib.pyplot as plt
import numpy as np
import json

timestamps_file = "export/timestamps_pipeline.log"
mem_prof_file = "export/pipeline_mem_c.log"
collectl_file = "export/collectl-simgrid-vm-20200324.dsk.csv"
input_size = "6000 MB"

f = open(mem_prof_file)
lines = f.readlines()

sys_mem = []
free_mem = []
used_mem = []
# app_mem = []
cache_used = []
avai_mem = []
dirty_ratio = []
dirty_bg_ratio = []
dirty_data = []

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

        dirty_amt_mb = int(values[12]) * 4096 / 2 ** 20
        dirty_data.append(dirty_amt_mb)

        available_mb = free_mem_mb + cache_in_mb - dirty_amt_mb
        avai_mem.append(available_mb)

        dirty_ratio.append(0.2 * available_mb)
        dirty_bg_ratio.append(0.1 * available_mb)

    else:
        if line.startswith("SWP"):
            values = line.split(" ")
            swap_size.append(int(values[7]) * 4096 / 2 ** 20)
            swap_free.append(int(values[8]) * 4096 / 2 ** 20)

intervals = len(dirty_data)
dirty_data = np.array(dirty_data)
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


time_stamp = {
    "read_start": [],
    "read_end": [],
    "write_start": [],
    "write_end": []
}

read_timestamp = {
    "read_start": [],
    "read_end": []
}

with open(timestamps_file) as time_stamp_file:
    lines = time_stamp_file.read().splitlines()

    for line in lines:
        part = line.split(":")
        time_stamp[part[0]].append(float(part[1]) / 1000)


def timestamp_plot(fig, time_stamps):
    read_start = time_stamps["read_start"]
    read_end = time_stamps["read_end"]
    write_start = time_stamps["write_start"]
    write_end = time_stamps["write_end"]
    start = read_start[0]

    for idx in range(len(read_start)):
        if idx == 0:
            fig.axvspan(xmin=read_end[idx] - start, xmax=write_start[idx] - start, color="k",
                        alpha=0.2, label="computation")
            fig.axvspan(xmin=0, xmax=read_end[idx] - start, color="g", alpha=0.2, label="read")
            fig.axvspan(xmin=write_start[idx] - start, xmax=write_end[idx] - start, color="b", alpha=0.2, label="write")
        else:
            fig.axvspan(xmin=read_end[idx] - start, xmax=write_start[idx] - start, color="k", alpha=0.2)
            fig.axvspan(xmin=read_start[idx] - start, xmax=read_end[idx] - start, color="g", alpha=0.2)
            fig.axvspan(xmin=write_start[idx] - start, xmax=write_end[idx] - start, color="b", alpha=0.2)


def timestamp_readonly_plot(fig, time_stamps):
    read_start = time_stamps["read_start"]
    read_end = time_stamps["read_end"]
    start = read_start[0]

    for idx in range(len(read_start)):
        fig.axvspan(xmin=read_start[idx] - start, xmax=read_end[idx] - start, color="g",
                    alpha=0.2)
        if idx < len(read_start) - 1:
            fig.axvspan(xmin=read_end[idx] - start, xmax=read_start[idx + 1] - start, color="k", alpha=0.2)


def mem_plot(fig, readonly=False):
    fig.minorticks_on()
    fig.set_title("memory profiling (input size = %s)" % input_size)

    if readonly:
        timestamp_readonly_plot(fig, time_stamp)
    else:
        timestamp_plot(fig, time_stamp)


    # app_cache = list(np.array(app_mem) + np.array(cache_used))

    fig.plot(time, sys_mem, color='k', linewidth=1.5, label="total mem")
    # ax1.plot(time, free_mem, color='g', linewidth=1.5, linestyle="-.", label="free memory")
    fig.plot(time, used_mem, color='g', linewidth=1.5, label="used mem")
    # ax1.plot(time, app_mem, color='c', linewidth=1.5, label="app memory")
    fig.plot(time, cache_used, color='m', linewidth=1.5, label="cache used")
    # ax1.plot(time, app_cache, color='c', linewidth=1.5, label="cache + app")
    fig.plot(time, dirty_data, color='r', linewidth=1.5, label="dirty data")
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


def collectl_plot(fig, readonly=False):
    dsk_data = np.loadtxt(collectl_file, skiprows=1, delimiter=',')
    read = dsk_data[:, 2] / 1024
    write = dsk_data[:, 6] / 1024

    time = np.arange(0, len(read))

    fig.minorticks_on()
    fig.set_title("disk throughput (MB)")

    if readonly:
        timestamp_readonly_plot(fig, time_stamp)
    else:
        timestamp_plot(fig, time_stamp)

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
