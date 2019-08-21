import sys
import time
import json
from pipeline import Pipeline
from export import export


def benchmark(input_filename):
    p = Pipeline(input_filename)

    rss = []
    runtime = []
    read_time = []
    write_time = []
    for j in range(0, 5):
        info = p.copy(input_filename, j)[Pipeline.STATS]
        rss.append(info[Pipeline.MEMORY])
        runtime.append(info[Pipeline.TOTAL_TIME])
        read_time.append(info[Pipeline.READING_TIME])
        write_time.append(info[Pipeline.WRITING_TIME])
        Pipeline.clean_output_folder()

    avg_rss = sum(rss) / len(rss)
    avg_read_time = sum(read_time) / len(read_time)
    avg_write_time = sum(write_time) / len(write_time)
    avg_runtime = sum(runtime) / len(write_time)

    print("Avg rss: {0:.0f} bytes".format(avg_rss))
    print("Max rss: {0} bytes".format(max(rss)))
    print("Avg runtime: {0:.4f} sec".format(sum(runtime) / len(runtime)))
    print("Avg read time: {0:.4f} sec".format(avg_read_time))
    print("Avg write time: {0:.4f} sec".format(avg_write_time))

    return {
        Pipeline.OUTPUT: input_filename,
        Pipeline.STATS: {
            Pipeline.MEMORY: avg_rss,
            Pipeline.TOTAL_TIME: avg_runtime,
            Pipeline.READING_TIME: avg_read_time,
            Pipeline.WRITING_TIME: avg_write_time
        }
    }


args = sys.argv
if len(args) < 2:
    print("Input file is required!")
else:
    stats = {}
    for i in range(1, len(args)):
        in_file = args[i]
        start = time.time()

        result = benchmark(in_file)
        stats[in_file] = result[Pipeline.STATS]

        end = time.time()
        print("\nTOTAL RUNTIME: {0:.4f}".format(end - start))

    export("export/" + args[0] + ".json", json.dumps(stats))
