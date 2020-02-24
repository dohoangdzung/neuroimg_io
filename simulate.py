dr = 160
dw = 150
mr = 6200
mw = 3400

dirty_background_ratio = 10
dirty_ratio = 20
sys_mem = 14500

cache_used = 0
used_mem = 0
dirty = 0

input_size = 6010
computation_time = 14

chunk = 100


class File:
    def __init__(self, name, size, size_in_disk, size_in_mem):
        self.name = name
        self.size = size
        self.size_in_disk = size_in_disk
        self.size_in_mem = size_in_mem
        self.dirty = 0


def read(file, used_mem, cache_used):
    time = 0
    read_from_disk = 0
    read_from_mem = 0

    # Read from disk
    while file.size_in_mem < file.size:
        read_amt = min(chunk, file.size - file.size_in_mem)

        time += read_amt / dr
        read_from_disk += read_amt
        file.size_in_mem += read_amt
        cache_used += read_amt
        used_mem += 2 * read_amt

    # Read from mem
    while read_from_mem < file.size:
        read_amt = min(chunk, file.size - read_from_mem)
        time += read_amt / mr
        read_from_mem += read_amt
        used_mem += read_amt

    return time, file


def write(file, cache_used, used_mem, dirty):
    time = 0
    size_in_cache = size_in_disk = 0

    return size_in_cache, size_in_disk, time, cache_used, used_mem, dirty


def evict(size):
    time = 0
    return time


file1 = File("file1", 6010, 6010, 0)
time, file1 = read(file1, used_mem, cache_used)
print("Time = %d s" % time)
print("File in cache %d MB, in disk %d MB" % (file1.size_in_mem, file1.size_in_disk))
