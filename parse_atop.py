import matplotlib.pyplot as plt
import numpy as np

f = open('export/pipeline_mem.log', 'r')
lines = f.readlines()

sys_mem = []
free_mem = []
cache_used = []
dirty_pages = []

swap_size = []
swap_free = []
# bw_r = []
# bw_w = []
for i in range(len(lines)):
    line = lines[i]
    if line.startswith("MEM"):
        values = line.split(" ")
        sys_mem.append(int(values[7]) * 4096 / 2 ** 20)
        free_mem.append(int(values[8]) * 4096 / 2 ** 20)
        cache_used.append(int(values[9]) * 4096 / 2 ** 20)
        dirty_pages.append(int(values[12]) * 4096 / 2 ** 20)
    else:
        if line.startswith("SWP"):
            values = line.split(" ")
            swap_size.append(int(values[7]) * 4096 / 2 ** 20)
            swap_free.append(int(values[8]) * 4096 / 2 ** 20)

intervals = len(dirty_pages)
dirty_pages = np.array(dirty_pages)
time = np.arange(0, intervals)


def plot_timeframe():
    plt.figure()
    plt.minorticks_on()
    plt.tight_layout()
    # ticks = list(plt.xticks()[0])
    # ticks.extend([0.43, 23.15, 53.12, 56.11, 92.01, 131.12, 162.73])
    # plt.xticks(ticks, rotation=75)
    # labels = list(plt.xticks()[1])
    # labels.extend([r'task1 read', r'task1 write', r"task2 read", r"task2 write", r"task3 read", r"task3 write",
    #                r"task3 write done"]))
    plt.axvline(x=0.31, linestyle=':', linewidth=1, color="b", label="task1 read")
    plt.axvline(x=23.83, linestyle=':', linewidth=1, color="b")

    plt.axvline(x=24.25, linestyle='--', linewidth=1, color="b", label="task1 write")
    plt.axvline(x=52.08, linestyle='--', linewidth=1, color="b")

    plt.axvline(x=53.81, linestyle=':', linewidth=1, color="c", label="task2 read")
    plt.axvline(x=56, linestyle=':', linewidth=1, color="c")

    plt.axvline(x=56.70, linestyle='--', linewidth=1, color="c", label="task2 write")
    plt.axvline(x=93.43, linestyle='--', linewidth=1, color="c")

    plt.axvline(x=95.58, linestyle=':', linewidth=1, color="y", label="task3 read")
    plt.axvline(x=134.32, linestyle=':', linewidth=1, color="y")

    plt.axvline(x=135.29, linestyle='--', linewidth=1, color="y", label="task3 write")
    plt.axvline(x=166.43, linestyle='--', linewidth=1, color="y")


plot_timeframe()
plt.title("read bw 266 MB/s , write bw ~ 164 MB/s")
plt.plot(time, sys_mem, color='k', linewidth=1.5, label="total memory")
plt.plot(time, free_mem, color='g', linewidth=1.5, label="free memory")
plt.plot(time, cache_used, color='m', linewidth=1.5, label="cache used")
plt.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
plt.legend()

plot_timeframe()
plt.title("read bw 269 MB/s , write bw 202 MB/s")
plt.plot(time, dirty_pages, color='r', linewidth=1.5, label="dirty data")
plt.legend()

plot_timeframe()
plt.title("swap")
plt.plot(time, swap_size, color='b', linewidth=1.5, label="swap size")
plt.plot(time, swap_free, color='g', linewidth=1.5, label="free swap")
plt.legend()

plt.show()
